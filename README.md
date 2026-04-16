Name: Girls Who Code Um-Dearborn HUb 
By Maha Ali and Alyamama Abdo

Purpose of the project: To create a seamless space for girls who code members on campus to view events happening, opportunities and connect
with other members and the eboard. Rather than using several platforms (some which require approval to post to members), we decided to 
create our own space to make it a better experience for our own members 

What was used:
Flask
SupaBase databse 
HTML, tailwindcss


Main components:
1. View mission Statements 
2. View Gallery composed of photos from past events
3. View upcoming events and past events, add events to calander and RSVP
4. Contact eboard members
5. Subscribe to newsletter
6. superAdmin login to publish new events and resources for members

HOW TO DEPLOY:
This application is built with Flask and uses a cloud-hosted **Supabase** (PostgreSQL) database. It is designed to be seamlessly deployed on platforms like [Render](https://render.com).
1. Prepare for Production
Flask's built-in development server cannot be used in production. Ensure the `gunicorn` WSGI server is installed and tracked in your project


pip install gunicorn
pip freeze > requirements.txt


Future Implementations: 
1. Email members when they RSVP
2. Allow admins to push articles
3. change photos/gallery from static to photos that admins can uplaod/change as well as the stats
4. complete the donation page
5. superAdmin is able to add admins and assign a new superAdmin

Design Patters and architectues used: 
1. decorative
2. Factory
3. Strategy
4. Observer
5. MVC 
