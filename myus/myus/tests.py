from datetime import datetime, timezone
from http import HTTPStatus

from django.urls import reverse
from django.test import TestCase

from myus.forms import NewHuntForm
from myus.models import Hunt, Puzzle, User


class TestViewHunt(TestCase):
    """Test the view_hunt endpoint

    The tests related to the handling of URLs with IDs and slugs should be taken as
    general tests for the redirect_from_hunt_id_to_hunt_id_and_slug decorator
    """

    def setUp(self):
        self.hunt = Hunt.objects.create(name="Test Hunt", slug="test-hunt")
        self.view_name = "view_hunt"

    def test_view_hunt_with_id_and_slug_success(self):
        """Visiting the view_hunt endpoint with both ID and slug in the URL displays the requested page"""
        res = self.client.get(
            reverse(self.view_name, args=[self.hunt.id, self.hunt.slug])
        )
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(res, "view_hunt.html")

    def test_view_hunt_with_id_only_redirects_to_id_and_slug(self):
        """Visiting the view_hunt endpoint with only ID in the URL redirects to the URL with ID and slug"""
        res = self.client.get(reverse(self.view_name, args=[self.hunt.id]))
        self.assertRedirects(
            res, reverse(self.view_name, args=[self.hunt.id, self.hunt.slug])
        )

    def test_view_hunt_with_id_and_wrong_slug_redirects_to_id_and_correct_slug(self):
        """Visiting the view_hunt endpoint with ID and the wrong slug in URL redirects to URL with ID and correct slug"""
        res = self.client.get(
            reverse(self.view_name, args=[self.hunt.id, "the-wrong-slug"])
        )
        self.assertRedirects(
            res, reverse(self.view_name, args=[self.hunt.id, self.hunt.slug])
        )


class TestViewPuzzle(TestCase):
    """Test the view_puzzle endpoint

    The tests related to the handling of URLs with IDs and slugs should be taken as general tests for the force_url_to_include_both_hunt_and_puzzle_slugs decorator
    """

    def setUp(self):
        self.hunt = Hunt.objects.create(name="Test Hunt", slug="test-hunt")
        self.puzzle = Puzzle.objects.create(
            name="Test Puzzle", slug="test-puzzle", hunt=self.hunt
        )
        self.view_name = "view_puzzle"
        self.correct_url = reverse(
            self.view_name,
            args=[self.hunt.id, self.hunt.slug, self.puzzle.id, self.puzzle.slug],
        )

    def test_view_puzzle_with_ids_and_slugs_success(self):
        """Visiting the view_puzzle endpoint with hunt and puzzle IDs and slug in the URL displays the requested page"""
        res = self.client.get(self.correct_url)
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(res, "view_puzzle.html")

    def test_view_puzzle_with_no_hunt_slug_redirects_to_full_url(self):
        """Visiting the view_puzzle endpoint with no hunt_slug in the URL redirects to the full URL"""
        res = self.client.get(
            reverse(
                self.view_name, args=[self.hunt.id, self.puzzle.id, self.puzzle.slug]
            )
        )
        self.assertRedirects(res, self.correct_url)

    def test_view_puzzle_with_no_puzzle_slug_redirects_to_full_url(self):
        """Visiting the view_puzzle endpoint with no puzzle_slug in the URL redirects to the full URL"""
        res = self.client.get(
            reverse(self.view_name, args=[self.hunt.id, self.hunt.slug, self.puzzle.id])
        )
        self.assertRedirects(res, self.correct_url)

    def test_view_puzzle_with_no_hunt_or_puzzle_slug_redirects_to_full_url(self):
        """Visiting the view_puzzle endpoint with no hunt_slug or puzzle_slug in the URL redirects to the full URL"""
        res = self.client.get(
            reverse(self.view_name, args=[self.hunt.id, self.puzzle.id])
        )
        self.assertRedirects(res, self.correct_url)

    def test_view_puzzle_with_ids_and_wrong_slugs_redirects_to_ids_and_correct_slugs(
        self,
    ):
        """Visiting the view_puzzle endpoint with IDs and the wrong slugs in URL redirects to URL with IDs and correct slugs"""
        res = self.client.get(
            reverse(
                self.view_name,
                args=[
                    self.hunt.id,
                    "wrong-hunt-slug",
                    self.puzzle.id,
                    "wrong-puzzle-slug",
                ],
            )
        )
        self.assertRedirects(res, self.correct_url)


class TestNewHuntForm(TestCase):
    """Test the NewHuntForm"""

    def setUp(self):
        self.shared_test_data = {
            "name": "Test Hunt",
            "slug": "test",
            "member_limit": 0,
            "guess_limit": 20,
            "leaderboard_style": "DEF",
            "solution_style": "VIS",
        }

    def test_hunt_form_accepts_start_time_in_iso_format(self):
        """The NewHuntForm accepts the start_time field in ISO format (YYYY-MM-DDTHH:MM:SS)"""
        test_data = self.shared_test_data.copy()
        start_time = datetime(2024, 3, 15, 1, 2, tzinfo=timezone.utc)
        test_data["start_time"] = start_time.isoformat()
        form = NewHuntForm(data=test_data)
        self.assertTrue(form.is_valid(), msg=form.errors)
        hunt = form.save()
        self.assertEqual(hunt.start_time, start_time)

    def test_hunt_form_accepts_start_time_without_seconds(self):
        """The NewHuntForm accepts the start_time field without seconds specified

        The out-of-the-box datetime-local input appears to provide data in this format
        """
        test_data = self.shared_test_data.copy()
        start_time = datetime(2024, 3, 15, 1, 2, tzinfo=timezone.utc)
        test_data["start_time"] = start_time.strftime("%Y-%m-%dT%H:%M")
        form = NewHuntForm(data=test_data)
        self.assertTrue(form.is_valid(), msg=form.errors)
        hunt = form.save()
        self.assertEqual(hunt.start_time, start_time)

    def test_hunt_form_start_time_uses_datetime_local_input(self):
        """The NewHuntForm uses a datetime-local input for the start_time field"""
        form = NewHuntForm(data=self.shared_test_data)
        start_time_field = form.fields["start_time"]
        self.assertEqual(start_time_field.widget.input_type, "datetime-local")

    def test_hunt_form_accepts_end_time_in_iso_format(self):
        """The NewHuntForm accepts the end_time field in ISO format (YYYY-MM-DDTHH:MM:SS)"""
        test_data = self.shared_test_data.copy()
        end_time = datetime(2024, 3, 15, 1, 2, tzinfo=timezone.utc)
        test_data["end_time"] = end_time.isoformat()
        form = NewHuntForm(data=test_data)
        self.assertTrue(form.is_valid(), msg=form.errors)
        hunt = form.save()
        self.assertEqual(hunt.end_time, end_time)

    def test_hunt_form_accepts_end_time_without_seconds(self):
        """The NewHuntForm accepts the end_time field without seconds specified

        The out-of-the-box datetime-local input appears to provide data in this format
        """
        test_data = self.shared_test_data.copy()
        end_time = datetime(2024, 3, 15, 1, 2, tzinfo=timezone.utc)
        test_data["end_time"] = end_time.strftime("%Y-%m-%dT%H:%M")
        form = NewHuntForm(data=test_data)
        self.assertTrue(form.is_valid(), msg=form.errors)
        hunt = form.save()
        self.assertEqual(hunt.end_time, end_time)

    def test_hunt_form_end_time_displays_datetime_local_widget(self):
        """The NewHuntForm uses a datetime-local input for the end_time field"""
        form = NewHuntForm(data=self.shared_test_data)
        end_time_field = form.fields["end_time"]
        self.assertEqual(end_time_field.widget.input_type, "datetime-local")
