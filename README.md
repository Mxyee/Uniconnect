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

### Register:
#### 1. Student – Register  
1. Click on the **Student Register** button.  
2. Students fill in their **username**, **email**, **password**, and **confirm password**.  
3. Click on the **Register** button.  
4. System checks for duplicate **username or email**.  
 - If duplicates are found, an error message is shown:  
  - **“Username already taken, please choose another.”**  
  - **“Email address already taken, please choose another.”**  
  - **“Passwords do not meet the security requirements.”**  
 - Otherwise, the student's account is created.  
5. Redirects to the **Login** page.

#### 2. Professor – Register (Admin only)  
1. Admin logs in.  
2. Click on the **Professor Register** button.  
3. Admin fills in the professor's **username**, **email**, **password**, and **confirm password**.  
4. Click on the **Register** button.  
5. System checks for duplicate **username or email**.  
 - If duplicates are found, an error message is shown:  
  - **“Username already taken, please choose another.”**  
  - **“Email address already taken, please choose another.”**  
 - Otherwise, the professor's account is created.  
6. Redirects to the **Login** page.

### Login:

#### 1. Student – Login  
1. Enter **username** and **password**.  
2. Click **Login**.  
- Successful login, navigate to the **Home** page.  
- Login failed: error message displayed:  
 **“Invalid username or password”**

#### 2. Professor – Login  
1. The professor account is created by **Admin** in advance.  
2. The **username** and **default password** are provided to the professor.  
3. Professor enters the username and default password.  
4. Click **Login**.
- Successful login: navigate to the **Home** page.  
- Login failed: error message displayed:  
 **“Invalid username or password”**

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
 • **“Invalid username or password”**  
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
 • **“Invalid username or password”**  
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

##### – Positive
**Scenario:** A student logs in and wants to organise a new study event.  
1. Students create an activity with a valid date (e.g., 7 days from today).  
2. Fill in all required fields.  
3. Click **"Create Activity"**.  
4. Redirects to the activity list page with a success message displayed.

##### – Negative
**Scenario:** A student tries to create an activity without meeting the date requirement.  
1. Attempt to create an activity using today’s date.  
2. Click **"Create Activity"**.  
3. Form stays on the same page and shows an error:  
  **“The activity date must be at least 7 days from today.”**


#### Test Case Two – Join Activity

##### – Positive
**Scenario:** A student wants to join a group event that is still open.  
1. Navigate to an activity that has available spots.  
2. Click **"Join Activity"**.  
3. Successfully joins and page refreshes, showing your name in the participant list.

##### – Negative
**Scenario:** A student tries to join a full activity.  
1. Attempt to join an activity that already has 5 participants.  
2. The **"Join Activity"** button is disabled and displays the text:  
  **“Activity Full”**


#### Test Case Three – Leave Activity

##### – Positive
**Scenario:** A student decides to leave an activity before the start date.  
1. Open an activity scheduled to start in 7 days.  
2. Click **"Leave"**.  
3. Successfully leaves with a confirmation message.

##### – Negative
**Scenario:** A student attempts to leave too close to the start of the activity.  
1. Attempt to leave an activity starting in 3 days.  
2. The **"Leave Activity"** button is disabled.
---
### Assignments, Submissions and Feedback:

#### 1. Professor – Create an Assignment
1. Navigate to the **Assignments** page from the navigation bar.  
2. Click the **New Assignment** button.  
3. Enter the **title**, **description**, and **deadline**.  
4. Click the **Submit** button.  
5. A success message will appear, and the assignment will be listed.  

#### 2. Professor – Search for Assignments
1. Navigate to the **Assignments** page from the navigation bar.  
2. Enter keywords in the **Search assignments** box.  
3. Click the **Search** button to search assignments by title with case-insensitive partial matches.  

#### 3. Professor – Edit an Assignment
1. On the **Assignments** page, click the title of the assignment you want to edit.  
2. On the assignment detail page, click the **Edit Assignment** button.  
3. Update the **title**, **description**, or **deadline**.  
4. Click **Submit** to save the changes.  

#### 4. Professor – Delete an Assignment
1. On the **Assignments** page, click the title of the assignment you want to delete.  
2. On the assignment detail page, click the **Delete Assignment** button.  
3. In the confirmation dialog, click **Confirm** to delete the assignment.  

#### 5. Student – Submit an Assignment
1. Navigate to the **Assignments** page.  
2. Click on the **title** of the assignment.  
3. On the assignment detail page, fill in your answer in the content box.  
4. Click **Submit Assignment**. A success message will confirm submission.  

#### 6. Student – Edit a Submission
1. On the assignment detail page, click **Edit Submission**.  
2. The form will be pre-filled with your existing answer.  
3. Modify your answer and click **Update Submission**.  
4. A success message confirms the update.  

#### 7. Student – Delete a Submission
1. On the assignment detail page, click **Delete Submission**.  
2. A confirmation dialog will appear. Click **OK** to delete.  
3. The submission will be removed from the system.  

#### 8. Student – View Feedback
1. After professor reviews the submission, feedback will be visible on the assignment detail page.  

#### 9. Professor – Give Feedback
1. On the assignment detail page, professors can view each submission.  
2. Enter comments in the feedback form and click **Submit** to save.  
3. The feedback becomes visible to the student.  

#### Test Case One – Student Submit Assignment

##### Positive
**Scenario:** Student submits an assignment successfully.  
1. Navigate to an assignment detail page.  
2. Enter valid answer text.  
3. Click **Submit Assignment**.  
4. Expect: “Submission saved” message appears.

##### Negative
**Scenario:** Student submits content that is too short.  
1. Enter a short answer (e.g., "short").  
2. Click **Submit Assignment**.  
3. Expect error: “Answer must be between 10 and 500 characters.”  
4. The page reloads without saving.

#### Test Case Two – Student Update Submission

##### Positive
**Scenario:** Student updates an existing submission.  
1. Click **Edit Submission**.  
2. Update the content with valid text.  
3. Click **Update Submission**.  
4. Expect message: “Submission updated successfully.”  
5. Content updated in both student and professor view.

##### Negative
**Scenario:** Student updates with invalid content length.  
1. Edit submission and input a short response (e.g., "tiny").  
2. Click **Update Submission**.  
3. Expect error message: “Answer must be between 10 and 500 characters.”  
4. Page stays on the same form without saving.
---
### Notifications:

## Implemented Functionalities

### Login and Register:
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
---
### Assignment Features:
1. Professors can create new assignments with title, description, and deadline.  
2. Professors can edit or delete assignments they created.
3. Professors can search assignments by title with case-insensitive partial matches.
4. Students can submit, edit, and delete their own assignment submissions.
5. Professors can view all student submissions and provide feedback for each one.
6. Submitted answers are pre-filled for editing convenience.
7. Only the student who submitted can modify or delete their own work.
8. Students can view professor feedback directly on the assignment detail page.
9. Professors can only edit their own assignments and cannot modify others’ assignments.
10. The answer must be between 10 to 500 characters.


## Contribution table
| Student Name & ID      | Contribution (%) | Key Contributions / Tasks Completed                                        | Signature     |
|------------------------|------------------|-----------------------------------------------------------------------------|---------------|
| Wenjung Chen / 2731069 | 20%              | Login and Register feature(student, professor) / HTML form / web design framework / film clips | Wenjung Chen  |
| Haoyang Zhao / 2731571 | 20%              | Create Assignments / Search Assignments / Edit Assignments / Delete Assignments / Registration (Backend) | Haoyang Zhao  |
| Ming-Ye Chan / 2748827 | 20%              | Student Submission / Edit Submission / Delete Submission / Professor Feedback/ Combine Project | Ming-Ye Chan  |
| Ting-Chieh Lin / 2744446 | 20%              | Create Activity / Edit Activity / Join Activity / Leave Activity / Delete Activity / Activity HTML Pages | Ting-Chieh Lin  |
| Ying-Hsin Hua / 2813747 | 20%              | Designed, styled, and implemented the complete Notification system / Integrated Flask-Mail, Mailtrap, and APScheduler with all notification functionalities | Ying-Hsin Hua  |

