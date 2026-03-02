from django.db import models

from apps.candidate.models import Candidate


class BatchRun(models.Model):

    scheduled_for = models.DateTimeField()
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)

    batch_size = models.IntegerField(default=0)
    success_count = models.IntegerField(default=0)
    failed_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Batch {self.id} - {self.scheduled_for}"


class CandidateAttempt(models.Model):

    class ResultStatus(models.TextChoices):
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"

    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name="attempts"
    )

    batch_run = models.ForeignKey(
        BatchRun, on_delete=models.CASCADE, related_name="attempts"
    )

    attempt_no = models.IntegerField()
    result_status = models.CharField(max_length=20, choices=ResultStatus.choices)

    error_message = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("candidate", "batch_run")
        indexes = [
            models.Index(fields=["candidate"]),
            models.Index(fields=["batch_run"]),
            models.Index(fields=["result_status"]),
        ]
