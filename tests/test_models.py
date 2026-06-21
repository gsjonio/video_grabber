"""Tests for vidgrab.models."""

from __future__ import annotations

from datetime import date

from vidgrab.models import VideoMetadata


_SAMPLE_INFO = {
    "id": "dQw4w9WgXcQ",
    "title": "Never Gonna Give You Up",
    "channel": "Rick Astley",
    "upload_date": "20091025",
    "duration": 212,
    "webpage_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "description": "The classic.",
    "tags": ["pop", "80s"],
    "license": "Standard YouTube License",
}


class TestVideoMetadataFromYtDlpInfo:
    def test_basic_fields(self) -> None:
        meta = VideoMetadata.from_yt_dlp_info(_SAMPLE_INFO)
        assert meta.video_id == "dQw4w9WgXcQ"
        assert meta.title == "Never Gonna Give You Up"
        assert meta.channel == "Rick Astley"
        assert meta.upload_date == date(2009, 10, 25)
        assert meta.duration_seconds == 212
        assert meta.url == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        assert meta.description == "The classic."
        assert meta.tags == ["pop", "80s"]

    def test_missing_channel_falls_back_to_uploader(self) -> None:
        info = {**_SAMPLE_INFO, "channel": None, "uploader": "Rick"}
        meta = VideoMetadata.from_yt_dlp_info(info)
        assert meta.channel == "Rick"

    def test_missing_duration_defaults_to_zero(self) -> None:
        info = {**_SAMPLE_INFO, "duration": None}
        meta = VideoMetadata.from_yt_dlp_info(info)
        assert meta.duration_seconds == 0

    def test_missing_tags_defaults_to_empty(self) -> None:
        info = {**_SAMPLE_INFO, "tags": None}
        meta = VideoMetadata.from_yt_dlp_info(info)
        assert meta.tags == []

    def test_missing_upload_date_defaults(self) -> None:
        info = {**_SAMPLE_INFO, "upload_date": None}
        info.pop("upload_date")
        meta = VideoMetadata.from_yt_dlp_info(info)
        assert meta.upload_date == date(1970, 1, 1)


class TestVideoMetadataToDict:
    def test_serializes_date_as_iso(self) -> None:
        meta = VideoMetadata.from_yt_dlp_info(_SAMPLE_INFO)
        d = meta.to_dict()
        assert d["upload_date"] == "2009-10-25"

    def test_contains_all_keys(self) -> None:
        meta = VideoMetadata.from_yt_dlp_info(_SAMPLE_INFO)
        d = meta.to_dict()
        assert set(d.keys()) == {
            "video_id", "title", "channel", "upload_date",
            "duration_seconds", "url", "description", "tags",
        }

    def test_tags_is_list(self) -> None:
        meta = VideoMetadata.from_yt_dlp_info(_SAMPLE_INFO)
        assert isinstance(meta.to_dict()["tags"], list)
