from django.db import models




class Board(models.Model):
    title = models.CharField(max_length=100)
    emails = models.CharField(max_length=100, blank=True)
    members = models.ManyToManyField('users.UserProfile', related_name='boards', blank=True)
    added_members = models.ManyToManyField('users.UserProfile', related_name='added_boards', blank=True)


    def __str__(self):
        return self.title
        





class Task(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=20, blank=True)
    due_date = models.DateField(null=True, blank=True)
    reviewer = models.CharField(max_length=100, blank=True)
    assignee = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, default='to-do')
    board = models.ForeignKey(Board, related_name='tasks', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    


class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.task.title}'