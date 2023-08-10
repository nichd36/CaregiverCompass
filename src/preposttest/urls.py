from django.urls import path
from preposttest.views import(
    pretest_view,
    pretest_data_view,
    save_pretest_view,
)

app_name = 'preposttest'

urlpatterns = [
    path('<slug>/pretest', pretest_view, name="pretest"),
    path('<slug>/pretest/data', pretest_data_view, name="pretest-data"),
    path('<slug>/pretest/save', save_pretest_view, name="save-data"),
]