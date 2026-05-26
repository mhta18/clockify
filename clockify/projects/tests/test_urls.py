import uuid
from projects.views import ProjctListAPIView, ProjctViewSet
from django.urls import resolve, reverse
from django.test import SimpleTestCase


class ProjectUrlTest(SimpleTestCase):
    def test_list_url_resolves_to_correct_view(self):
        url_match = resolve("/api/projects/list/")

        self.assertEqual(url_match.func.cls, ProjctListAPIView)

    def test_detail_url_resolves_with_uuid_base_name(self):
        mock_uuid = str(uuid.uuid4())
        target_path = reverse("projects-detail", kwargs={"pk": mock_uuid})
        url_match = resolve(target_path)
        self.assertEqual(url_match.func.cls, ProjctViewSet)
        self.assertEqual(url_match.kwargs["pk"], mock_uuid)
        self.assertEqual(url_match.func.actions["get"], "retrieve")
