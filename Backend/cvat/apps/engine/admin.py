from django.contrib import admin

from .models import Task, Segment, Job, Label, AttributeSpec, Log
from .models import LabeledImage, LabeledImageAttributeVal, LabeledShape, LabeledShapeAttributeVal


class JobInline(admin.TabularInline):
    model = Job
    can_delete = False

    # 不显示要添加对象的额外行
    def has_add_permission(self, request, object=None):
        return False


class SegmentInline(admin.TabularInline):
    model = Segment
    show_change_link = True
    readonly_fields = ('start_frame', 'stop_frame')
    can_delete = False

    # 不显示要添加对象的额外行
    def has_add_permission(self, request, object=None):
        return False


class AttributeSpecInline(admin.TabularInline):
    model = AttributeSpec
    extra = 0
    max_num = None


class LabelInline(admin.TabularInline):
    model = Label
    show_change_link = True
    extra = 0
    max_num = None


class LabelAdmin(admin.ModelAdmin):
    # 不显示在管理索引页上
    def has_module_permission(self, request):
        return False

    inlines = [
        AttributeSpecInline
    ]


class SegmentAdmin(admin.ModelAdmin):
    # 不显示在管理索引页上
    def has_module_permission(self, request):
        return False

    inlines = [
        JobInline
    ]


class TaskAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated_date'
    readonly_fields = ('created_date', 'updated_date', 'overlap')
    list_display = ('name', 'mode', 'owner', 'assignee', 'created_date', 'updated_date')
    search_fields = ('name', 'mode', 'owner__username', 'owner__first_name', 'owner__last_name', 'owner__email',
                     'assignee__username', 'assignee__first_name', 'assignee__last_name')
    inlines = [
        SegmentInline,
        LabelInline
    ]

    # 不允许添加任务，因为它不是简单的操作
    def has_add_permission(self, request):
        return False


admin.site.register(Task, TaskAdmin)
admin.site.register(LabeledImage)
admin.site.register(LabeledImageAttributeVal)
admin.site.register(LabeledShape)
admin.site.register(LabeledShapeAttributeVal)
admin.site.register(Job)
admin.site.register(Log)
