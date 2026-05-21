from django.http import JsonResponse, HttpResponse


def api_root(request):
	if 'text/html' in request.headers.get('Accept', ''):
		return HttpResponse(
			"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>CourseForces API</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 36rem; margin: 3rem auto; padding: 0 1rem; line-height: 1.5; }
    h1 { font-size: 1.25rem; }
    a { color: #0b5; }
    ul { padding-left: 1.25rem; }
    .note { color: #555; font-size: 0.9rem; margin-top: 2rem; }
  </style>
</head>
<body>
  <h1>CourseForces API</h1>
  <p>Backend is running. This server is the <strong>API</strong>, not the student app.</p>
  <ul>
    <li><a href="/admin/">Django Admin</a> — view users, courses, quizzes, submissions</li>
    <li><a href="http://localhost:4225">React app</a> — sign in / student &amp; professor UI</li>
  </ul>
  <p class="note">Admin login uses a <strong>Django superuser</strong> account (<code>createsuperuser</code>), not the same password as app sign-in.</p>
</body>
</html>""",
			content_type='text/html',
		)

	return JsonResponse({
		'status': 'ok',
		'message': 'CourseForces API is running.',
		'endpoints': {
			'admin': '/admin/',
			'users': '/users/',
			'courses': '/courses/',
			'quiz': '/quiz/',
		},
	})
