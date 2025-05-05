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


### Activities:

1. **Student – Creating an Activity**  

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

---

2. **Student – Edit an Activity (Creator Only)**

   1. On the **Activities** page, find the activity you created.  
   2. Click **Details** to open the activity detail page.  
   3. If you're the creator, you will see an **Edit** button.  
   4. Click **Edit**, update the fields as needed, and then click **Create Activity**.  
   5. A success message will confirm the updates.  

   **Note:** You cannot edit activities that have already taken place.  

---

3. **Student – Participate in an Activity**

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

---

4. **Professor**

   1. Professors can view all activities, including details and participant lists.  
   2. However, professors **cannot create, join, edit, or leave** activities.  


## Implemented Functionalities

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

