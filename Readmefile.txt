<-- copy+past directed # comment  -->

----- setup project ----
---create virtual environment
	# pip install django
 	# py -m venv venv
	# .\venv\Scripts\activate
	# pip install -r requirements.txt
	# python manage.py runserver

---Check Output on this url
	# http://127.0.0.1:8000/

--- superuser 
	# http://127.0.0.1:8000/admin
	# username = admin
	# password = 321



--- Input for api  ---
<-- i used thunderclient for api testing -->

-----register user
	# method POST
	# url http://127.0.0.1:8000/register/
	# Json content
	{
    "username":"user1",
    "password":"321",
    "password2":"321",
    "user_full_name":"user1 user1"
	}
	or 
	# you can used -> body -> form
	# filedname is -> username , password , password2 , user_full_name
o/p -  "user has registered successfully

-----login user
	# method POST
	# url http://127.0.0.1:8000/login/
	# json content
	{
    "username":"admin",
    "password":"321"
	}

-----user can edit userfullname
	# method POST
	# url http://127.0.0.1:8000/edituser/
	-- pass token in header
	# Authorization Token enter_token_here
	# json content
	{
    "user_full_name":"pankaj sajekar"
}	
	or 
	# user you can used -> body -> form
	fieldname = user_full_name
	value = enter_name
o/p- "response": "User fullname updated. previous name is Pankaj updated name is pankaj sajekar"


-----user1 send friend request to other  
	# method POST
	# url http://127.0.0.1:8000/sendrequest/1/
	-- pass token in header
	-- Authorization Token enter_token_here
o/p- "friend request is send to admin"


-----user2 login accept the friend request 
	# method POST
	# url http://127.0.0.1:8000/AccepetRejectRequest/
	-- pass token in header
	# Authorization Token enter_token_here
	# json content ( requestid -> request id can see in admin panel & requeststatus choices -> 1. accept 2. reject )
	{
    "requestid":"7",
    "requeststatus":"reject"
}
	or 
	# user you can used -> body -> form
	# field name is 1. requestid    2. requeststatus

o/p-  "response": "friend request 7 is reject"


-----logout user
	# method GET
	# url http://127.0.0.1:8000/logout/
	-- pass token in header
	# Authorization Token enter_token_here
o/p- "User Logged out successfully"

-----user account delete
	# method GET
	# url http://127.0.0.1:8000/accdelete/
	-- pass token in header
	# Authorization Token enter_token_here
o/p- "User Account Deleted"