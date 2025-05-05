# Uniconnect
## System description
## Programming languages & Frameworks Used
- Python 3.x  
- Flask  
- Jinja2  
- Flask-WTF  
- Flask-Mail  
- JavaScript  
- Bootstrap 5  
- HTML/CSS  
- SQLAlchemy  
- SQLite  
- APScheduler
## Step by step instruction

### Register
#### Student – Register  
Click on the **Student Register** button.  
Students fill in their **username**, **email**, **password**, and **confirm password**.  
Click on the **Register** button.  
System checks for duplicate **username or email**.  
 - If duplicates are found, an error message is shown:  
  - **“Username already taken, please choose another.”**  
  - **“Email address already taken, please choose another.”**  
  - **“Passwords do not meet the security requirements.”**  
 - Otherwise, the student's account is created.  
Redirects to the **Login** page.

#### Professor – Register (Admin only)  
Admin logs in.  
Click on the **Professor Register** button.  
Admin fills in the professor's **username**, **email**, **password**, and **confirm password**.  
Click on the **Register** button.  
System checks for duplicate **username or email**.  
 - If duplicates are found, an error message is shown:  
  - **“Username already taken, please choose another.”**  
  - **“Email address already taken, please choose another.”**  
 - Otherwise, the professor's account is created.  
Redirects to the **Login** page.

### Login

#### Student – Login  
Enter **username** and **password**.  
Click **Login**.  
- After successful login: navigate to the **Home** page.  
- Failed login:  
 **An error message is displayed (wrong account or password).**

#### Professor – Login  
The professor account is created by **Admin** in advance.  
The **username** and **default password** are provided to the professor.  
Professor enters the username and default password.  
Click **Login**.  
- Successful login: navigate to the **Home** page.  
- Login failed: error message displayed:  
 **“Incorrect account or password.”**

#### Test Case One – Registers and Login

##### – Positive  
**Scenario**: Student registers with valid information and logs in successfully.  
1. Navigate to the **Student Register** page.  
2. Fill in the registration form:  
 • Username: `Alice886`  
 • Email: `alice66@gmail.com`  
 • Password: `Hello123`  
 • Confirm Password: `Hello123`  
3. Click the **Register** button.  
4. Registration is successful. Redirects to the **Login** page.  
5. On the **Login** page, enter:  
 • Username: `Alice886`  
 • Password: `Hello123`  
6. Click the **Login** button.  
7. Login is successful. User is navigated to the **Home** page.

##### – Negative  
**Scenario**: Student attempts to log in with incorrect credentials.  
1. Navigate to the **Student Login** page.  
2. Enter:  
 • Username: `Alice886`  
 • Password: `www234`  
3. Click the **Login** button.  
4. Login fails. An error message is displayed:  
 • **“Incorrect username or password.”**  
5. The user remains on the login page.

#### Test Case Two – Professor Login

##### – Positive  
**Scenario**: Professor logs in with valid credentials.  
1. Admin creates a professor account with:  
 • Username: `prof.A`  
 • Password: `Prof12345`  
2. Professor navigates to the **Professor Login** page.  
3. Enters:  
 • Username: `prof.A`  
 • Password: `Prof12345`  
4. Click the **Login** button.  
5. Login is successful. The professor is navigated to the **Home** page.

##### – Negative  
**Scenario**: Professor enters incorrect login information.  
1. Navigate to the **Professor Login** page.  
2. Enter:  
 • Username: `prof.A`  
 • Password: `12345`  
3. Click the **Login** button.  
4. Login fails. An error message is displayed:  
 • **“Incorrect account or password, not in the record.”**  
5. The professor remains on the login page.

---
### Activities:

#### 1. Student – Creating an Activity

1. Navigate to the Activities page from the navigation bar.  
2. Click the **Create New Activity** button.  
3. Fill out the required fields:  
   - **Title:** Enter a descriptive title for the activity.  
   - **Description:** Provide details about the activity.  
   - **Location:** Select a location from the dropdown menu.  
     (If “Other” is selected, you may manually enter a custom location.)  
   - **Date and Time:** Choose a date at least **7 days from today**.  
4. Click **Create Activity** to create the activity.  
5. A confirmation message will appear once the activity is successfully created.  

**Note:** Upon creation, the student is automatically registered as a participant of the activity.  


#### 2. Student – Edit an Activity (Creator Only)

1. On the **Activities** page, find the activity you created.  
2. Click **Details** to open the activity detail page.  
3. If you're the creator, you will see an **Edit** button.  
4. Click **Edit**, update the fields as needed, and then click **Create Activity**.  
5. A success message will confirm the updates.  

**Note:** You cannot edit activities that have already taken place.  


#### 3. Student – Participate in an Activity

1. On the **Activities** page, browse or search for activities.  
2. Click **Details** on any activity to see its description, time, and current participants.  
3. Use the **Join** button to participate in an activity.  
4. If the activity is full (5 participants), a warning will be shown.  
5. To **leave** an activity:  
   - Go to the activity details.  
   - Click **Leave** (only allowed if the activity is more than 3 days away).  
   - A confirmation message will appear upon successful leave.  

**Note:**  
- If the original creator leaves and there are still participants, the system will automatically assign the next participant in order as a new creator.  
- If no participants remain, the activity will be automatically deleted.  


#### 4. Professor

1. Professors can view all activities, including details and participant lists.  
2. However, professors **cannot create, join, edit, or leave** activities.


#### Test Case One – Create Activity

##### Positive
**Scenario:** A student logs in and wants to organise a new study event.  
1. Students create an activity with a valid date (e.g., 7 days from today).  
2. Fill in all required fields.  
3. Click **"Create Activity"**.  
4. Redirects to the activity list page with a success message displayed.

##### Negative
**Scenario:** A student tries to create an activity without meeting the date requirement.  
1. Attempt to create an activity using today’s date.  
2. Click **"Create Activity"**.  
3. Form stays on the same page and shows an error:  
  **“The activity date must be at least 7 days from today.”**


#### Test Case Two – Join Activity

##### Positive
**Scenario:** A student wants to join a group event that is still open.  
1. Navigate to an activity that has available spots.  
2. Click **"Join Activity"**.  
3. Successfully joins and page refreshes, showing your name in the participant list.

##### Negative
**Scenario:** A student tries to join a full activity.  
1. Attempt to join an activity that already has 5 participants.  
2. The **"Join Activity"** button is disabled and displays the text:  
  **“Activity Full”**


#### Test Case Three – Leave Activity

##### Positive
**Scenario:** A student decides to leave an activity before the start date.  
1. Open an activity scheduled to start in 7 days.  
2. Click **"Leave"**.  
3. Successfully leaves with a confirmation message.

##### Negative
**Scenario:** A student attempts to leave too close to the start of the activity.  
1. Attempt to leave an activity starting in 3 days.  
2. The **"Leave Activity"** button is disabled.

---
## Implemented Functionalities

#### Implemented Login and Register

1. Students can register their own accounts via the **Student Register** page.  
2. The system validates duplicate **username** and **email** during registration.  
3. Password confirmation is required and must match the original password.  
4. Passwords must meet the policy requirements:  
 - Minimum 8 characters  
 - At least one uppercase letter  
 - At least one lowercase letter  
 - At least one number  
5. On successful registration, students are redirected to the **Login** page.  
6. Admins can create professor accounts via the **Professor Register** page.  
7. Professors cannot register themselves; accounts are provided by **Admin**.  
8. Both students and professors can log in using their assigned credentials.  
9. Login process validates **username** and **password**.  
10. Invalid login attempts display clear error messages and do not proceed.  
11. Successful login redirects to the **Home** page.  
12. The system distinguishes login types between **Student** and **Professor**.

---

### Activity Features:

1. Students can create activities.  
2. The activity creator can edit the activity.  
3. If the creator leaves the activity, the next participant automatically becomes the new creator.  
4. If the last participant leaves the activity, the activity is deleted.  
5. Any student can join an activity at any time.  
6. Students can only leave an activity if it is at least 3 days before the activity starts.  
7. Activities can only be created with a start date that is at least 7 days in the future.  
8. Activities can be searched and sorted by title, date, and location.  
9. Students can view all activities they have joined by clicking "Show My Activities".  
10. Each activity has a maximum of 5 participants.  
11. Students cannot join past activities.  

## Contribution table
| Student Name & ID      | Contribution (%) | Key Contributions / Tasks Completed                                        | Signature     |
|------------------------|------------------|-----------------------------------------------------------------------------|---------------|
| Wenjung Chen / 2731069 | 20%              | Login and Register feature(student, professor) / HTML form / web design framework / film clips | Wenjung Chen  |
| Haoyang Zhao / 2731571 | 20%              | Create Assignments / Search Assignments / Edit Assignments / Delete Assignments / Registration (Backend) | Haoyang Zhao  |
| Ming-Ye Chan / 2748827 | 20%              | Student Submission / Edit Submission / Delete Submission / Professor Feedback/ Combine Project | Ming-Ye Chan  |
| Ting-Chieh Lin / 2744446 | 20%              | Create Activity / Edit Activity / Join Activity / Leave Activity / Delete Activity / Activity HTML Pages | Ting-Chieh Lin  |
| Ying-Hsin Hua / 2813747 | 20%              | Designed, styled, and implemented the complete Notification system / Integrated Flask-Mail, Mailtrap, and APScheduler with all notification functionalities | Ying-Hsin Hua  |

