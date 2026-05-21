```
virtualenv cs315_virtualenv
source cs315_virtualenv/bin/activate
```

## API documentation

```
Output format = will receive a status 200 when succesfull else some status for error with error message
```

### Users

1) 
```
Route - /users/register/
Task - It registers a new user onto the website
METHOD - POST
Input format = {
	"name":<string>,
	"username":<string>,
	"department":one of the following "CSE","MSE","AE","ME","EE",
	"email":<email>,
	"password":<string>,
	"confirm_password":<string>
}
```

2) 
```
Route - /users/auth/login/
Task - It logins a user onto the website
METHOD - POST
Input format = {
	"value":<string(for username)/email(for email)>,
	"password":<string>
}

In output format will receive a token if succesfull
```

3) 
```
Route - /users/auth/logout/
Task - It logout a user from the website
METHOD - POST
Headers should contain "Authorization" field which stores the token
Input format = {}

Remove the token stored and then make it empty
```


4) 
```
Route - /users/password/forgot/1/
Task - It sends a mail to the user to reset the password
METHOD - POST
Input format = {
	"value":<string(for username)/email(for email)>
}

```

5) 
```
Route - /users/password/forgot/1/
Task - It sends a mail to the user to reset the password
METHOD - POST
Input format = {
	"value":<string(for username)/email(for email)>
}

```

6) need to discuss this , can be left for now . First lets integrate the rest.
```
Route - /users/password/forgot/2/<str:username>/code=<str:code>/
Method = POST
Input Format = {
	"new_password1":<a string>,
	"new_password2":<a string>
}

```

### Course

1)
```
Route - /courses/create/
Task - It creates a new course
METHOD - POST
Headers should contain "Authorization" field which stores the token
Input format = {
	"course_code":<string>,
	"course_name":<string>,
	"offered_year":<string>
}

Refetch the whole the courses here to get the update list 

```

2)
```
Route - /courses/join/request/send/
Task - It sends a join course request to the person
METHOD - POST
Headers should contain "Authorization" field which stores the token
Input format = {
	"course_pk":<int>,
	"send_to_user":<string username of the >,
	"join_as_role":"S" or "P" 
}

```

Acceptance is done by the email sent to the send_to_user

3) 

```
Route - /courses/my/list/
Task - It shows the list of user courses
Headers should contain "Authorization" field which stores the token
METHOD - GET

Output Format = 
[
    {
        "id": 18,
        "user_id": 14,
        "course_id": 3,
        "role": "P",
        "request_accepted": true,
        "verification_code": null 
    },
    {
        "id": 19,
        "user_id": 14,
        "course_id": 4,
        "role": "S",
        "request_accepted": true,
        "verification_code": null
    },
    
]
```

Here ignore the "verification_code" field

4) 
```
Route - /courses/list/<int:course_pk>/
Task - It shows the list of user in a particular course
Headers should contain "Authorization" field which stores the token
METHOD - GET

Output format
[
    {
        "user_id": 14,
        "role": "P",
        "request_accepted": true,
        "username": "agshubh",
        "name": "Shubh"
    },
    {
        "user_id": 18,
        "role": "S",
        "request_accepted": true,
        "username": "shubh101295",
        "name": "shubh1012"
    }
]
```

### Quiz

```
Route - /quiz/add/
Task - It adds a quiz in a particular course
Headers should contain "Authorization" field which stores the token
METHOD - POST

Input Format = {
    "title":<string>,
    "content":<string>,
    "course_pk":<int>,
    "deadline":<YYYY-MM-DDThh:mm>,
    "start_at":<YYYY-MM-DDThh:mm>
}

On success
{
    "quiz_pk": 12, # it here is the integer which is returned 
    "message": "Succesully created Quiz"
}
```

```
Route - /quiz/view/<int:course_pk>/
Task - It return the list of quiz in a particular course
Headers should contain "Authorization" field which stores the token
METHOD - GET

Input Format = {}

Output 
{
    "quiz_list": [
        {
            "pk": 12,
            "title": "Quiz 1 in CS315",
            "content": "Please score positive",
            "deadline": "2022-12-12T11:11:00Z",
            "start_at": "2022-12-12T11:11:00Z"
        },
        ......
    ],
    "message": "ok"
}
```

```
Route - /quiz/question/add/
Task - It adds a question to quiz in a particular course
Headers should contain "Authorization" field which stores the token
METHOD - POST

Input Format = {
    "course_pk":<int>,
    "quiz_pk":<int>,
    "content":<string>,
    "answer":<string>, # empty in case of MCQ and MSQ
    "positive_marks":<float>,
    "negative_marks":<float>,
    "question_type": "S", "M" or "F"
    ## ("S" , "MCQ Single Correct"),
    ##  ("M" , "MCQ Multi Correct"),
    ##  ("F" , "Fill in the blank") 
    "partial_allowed":<boolean>,
    
    ## following only in case of MCQ and MSQ
    "options":[
        {
            "option_value":<string>,
            "is_correct":<bool>
        }
        ....
        {
            "option_value":<string>,
            "is_correct":<bool>
        }
    ]
}


eg 1 

{
    "content":"This is Q2",
    "course_pk":5,
    "quiz_pk":12,
    "question_type":"S",
    "positive_marks":2.0,
    "negative_marks":0.5,
    "partial_allowed":false,   
    "answer":"",
    "options":[
        {
            "option_value":"yes",
            "is_correct":true
        },
        {
            "option_value":"no",
            "is_correct":false
        }
    ]
}



eg2

{
    "content":"This is Q4",
    "course_pk":5,
    "quiz_pk":12,
    "question_type":"F",
    "positive_marks":2.0,
    "negative_marks":0.5,
    "partial_allowed":false,   
    "answer":"No"
    
}

On success
{
    "question_pk": 12, # it here is the integer which is returned 
    "message": "Succesully created Question"
}

```

```
Route - /quiz/question/delete/
Task - It deletes a question to quiz in a particular course
Headers should contain "Authorization" field which stores the token
METHOD - DELETE

Input Format = {
    "course_pk":<int>,
    "quiz_pk":<int>,
    "question_pk":<int>
}

On success
{
    "message": "Succesfully deleted the question"
}
```

```
Route - /quiz/view/<int:course_pk>/<int:quiz_pk>/
Task - It lists all the question in the quiz

Headers should contain "Authorization" field which stores the token
METHOD - GET

Input Format = {}


Output format

{
    "title": "Quiz 1 in CS315",
    "content": "Please score positive",
    "start_at": "2022-12-12T11:11:00Z",
    "deadline": "2022-12-12T11:11:00Z",
    "questions": [
        {
            "question_pk": 12,
            "content": "This is Q1",
            "question_type": "F",
            "positive_marks": 2.0,
            "negative_marks": 0.5,
            "partial_allowed": false
        },
        {
            "question_pk": 13,
            "content": "This is Q2",
            "question_type": "S",
            "positive_marks": 2.0,
            "negative_marks": 0.5,
            "partial_allowed": false,
            "options": [
                {
                    "option_value": "yes",
                    "option_pk": 35
                },
                {
                    "option_value": "no",
                    "option_pk": 36
                }
            ]
        },
        {
            "question_pk": 14,
            "content": "This is Q4",
            "question_type": "F",
            "positive_marks": 2.0,
            "negative_marks": 0.5,
            "partial_allowed": false
        }
    ]
}
```

```
Route - /quiz/make/submission/
Task - It makes a submission of the student for the quiz

Headers should contain "Authorization" field which stores the token
METHOD - POST

Input format
{
    "course_pk":<int>,
    "quiz_pk":<int>,
    "ques_response":[
        {
            "question_pk":<int>,
            "answer":<string for Fill ups, list of option_pks for Single or Multi correct>
        },
        ...
    ]
}

eg.
{
    "course_pk":5,
    "quiz_pk":12,
    "ques_response":[
        {
            "question_pk":12,
            "answer":"Yes"
        },
        {
            "question_pk":13,
            "answer":[36]
        },
        {
            "question_pk":14,
            "answer":"no"
        }
    ]
}


On success Output

{
    "message": "Succesully submitted the quiz response",
    "quiz_attempt_pk": 11
}

```

```
Route - /quiz/show/marks/list/<int:course_pk>/<int:quiz_pk>/
Task - It shows marks list of student for the quiz

Headers should contain "Authorization" field which stores the token
METHOD - POST

Output = 
[
    {
        "name": "shubh1012",
        "username": "shubh101295",
        "user_pk": 18,
        "total_marks": 1.5
    },
    {
        "name": "shubh10122",
        "username": "shubh12301295",
        "user_pk": 19,
        "total_marks": 2.0
    }
]
```

```
Route = /quiz/marks/calculate/
Task - Calculate marks of all the students
Headers should contain "Authorization" field which stores the token
METHOD - POST

Input format
{
    "course_pk":<int>,
    "quiz_pk":<int>
}
```

```
Route = /quiz/delete/
Task - Delete a quiz
Headers should contain "Authorization" field which stores the token
METHOD - DELETE

Input format
{
    "course_pk":<int>,
    "quiz_pk":<int>
}
```

```
Route = /quiz/delete/course/
Task - Delete a course
Headers should contain "Authorization" field which stores the token
METHOD - DELETE

Input format
{
    "course_pk":<int>
}
```
