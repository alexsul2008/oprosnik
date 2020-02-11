from django.contrib import admin
from django.forms import Textarea
from django.utils.safestring import mark_safe


from .models import Questions, Answers, UsersAnswer




class AnswerInline(admin.TabularInline):
    model = Answers
    extra = 1

@admin.register(Questions)
class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ("get_image_tab", "get_image")
    #Поля выводимые в разделе Вопросы
    list_display = ("id", "description", "get_image", "in_active", "groups")
    list_filter = ("groups", "in_active",)

    # Поля которое выполняет свойство редактирования
    list_display_links = ("description",)
    # Вывод кнопок сохранения в верхней части страницы
    save_on_top = True

    # Включение возможности переключения Активный/Не активный вопрос
    list_editable = ("in_active", "groups",)
    actions = ["activate", "deactivate"]



    fieldsets = [
        (None, {
            'fields': [('description', 'get_image_tab'),]
        }),
        (None, {
            'fields': ['in_active', 'groups']
        }),
        (None, {
            'fields': ['image']
        }),
        (None, {
            'fields': ['doc_url']
        }),
    ]
    inlines = [AnswerInline]

    class Meta:
        model = Questions
        fields = "__all__"


    @mark_safe
    def get_image(self, obj):
        #return mark_safe(f'<img src="{obj.image.}" width="100" height="60" ')
        #return mark_safe('<img src="{obj.image}" />' % obj.image)
        return f'<img src="{obj.image.url}" width="80" />' if obj.image else ''
    get_image.short_description = "Изображение"

    @mark_safe
    def get_image_tab(self, obj):
        return f'<img src="{obj.image.url}" width="200" />' if obj.image else ''
    get_image_tab.short_description = "Изображение"


    def activate(self, request, queryset):
        row_update = queryset.update(in_active=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записи(ей) было(и) обновлены"
        self.message_user(request, f"{message_bit}")


    def deactivate(self, request, queryset):
        row_update = queryset.update(in_active=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записи(ей) было(и) обновлены"
        self.message_user(request, f"{message_bit}")

    activate.short_description = "Сделать выделенные вопросы активными"
    activate.allowed_permissions = ('change',)

    deactivate.short_description = "Сделать выделенные вопросы не активными"
    deactivate.allowed_permissions = ('change',)


@admin.register(UsersAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_key', )
    list_filter = ('user', )
    ordering = ('session_key', )
    # raw_id_fields = ('user', )

    class Meta:
        model = UsersAnswer
        fields = "__all__"


#admin.site.register(Questions, QuestionAdmin)

admin.site.site_title = "Опросник теоретический знаний"
admin.site.site_header = "Опросник теоретический знаний"