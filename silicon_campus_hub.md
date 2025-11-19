# 📣 S I L I C O N - C A M P U S  🛰️ H U B

> **Smart. Secure. Student-Centric.**  
> A modular FastAPI-based student platform featuring Announcements, Authentication, and Lost & Found.

---

## 👥 Team Directory

| 👤 Name               | 🆔 Silicon ID | 📧 Email                   |
|-----------------------|----------------|-----------------------------|
| Ashutosh Mohanty      | 24BCSA25       | cse.24bcsa25@silicon.ac.in  |
| Sandeep Kumar Sahoo   | 24BECF91       | ece.24becf91@silicon.ac.in  |
| Asmit Raj             | 24BCSI64       | cse.24bcsi64@silicon.ac.in  |
| Ashutosh Das          | 24BCSF49       | cse.24bcsf49@silicon.ac.in  |
| Sikhar Sambhab Mund   | 24BECB50       | ece.24becb50@silicon.ac.in  |

---

## 📌 What Has Been Done & How

| Module              | What We Did                                                                 | How It Was Done                                                                                      |
|---------------------|------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| 🔐 Authentication    | Implemented login, registration, and JWT-based session handling             | Used FastAPI dependencies and `OAuth2PasswordBearer` with JWT token generation and role-based access  |
| 📣 Announcements     | Enabled admins to post, view, and delete announcements                      | Built CRUD endpoints using FastAPI with admin-only authorization middleware                           |
| 🎒 Lost & Found      | Created features to post and browse lost/found items                        | Used same structure as announcements; included title, description, image, and user ownership fields   |
| 🧠 Password Check    | Enforced strong passwords on user registration                              | Created a custom validator checking length, cases, digits, and special characters                     |
| 🧪 Swagger Testing   | Explored and verified API endpoints                                          | Enabled `/docs` via FastAPI's built-in Swagger integration                                            |
| 🛠️ Git Management    | Organized project structure, branches, commits                              | Used Git + GitHub with branching strategy, commit naming, and pull request reviews                    |

---

## ⚙️ Roles & Responsibilities

---

### ⚡ **[Ashutosh Mohanty](https://github.com/Ashutosh-1505) – The Architect**

> _Laid the project's foundation with clean Git workflows and repo structure, while engineering the POST logic that powers Lost & Found submissions._

#### 🧩 Features

- 🛰️ **[Git Management](https://github.com/Syllogistek-System/silicon-campus-hub-team-10/tree/lost_found)**  
  Managed silicon_campus_hub.md, pull requests, and repo hygiene.

- 🎒 **[Lost & Found: POST Endpoint](https://github.com/Syllogistek-System/silicon-campus-hub-team-10/blob/lost_found/app/services/lost_found.py)**  
  Designed and built the main POST API for Lost & Found entries and Password Strength checker.

- 📬 **[Contact](mailto:cse.24bcsa25@silicon.ac.in)**

- 🛠️ **How it was done**: The `POST` endpoint allows only admin users to submit lost or found items. It uses payload validation, role-based access control, and `SQLAlchemy ORM` to securely save the item to the database. Each post is linked to the user who created it and returns key details in a `201` Created response.


#### 💻 Lost & Found – POST API Code

```python
@router.post("/admin/lost_found", status_code=201)
def create_lost_found(
    payload: lost_Found_Item,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    lost_found = LostFoundItem(
        title=payload.title,
        description=payload.description,
        is_found=payload.is_found,
        created_by=current_user.id
    )
    db.add(lost_found)
    db.commit()
    db.refresh(lost_found)
    return {
        "message": "Lost and Found created",
        "id": lost_found.id,
        "title": lost_found.title,
        "is_found": lost_found.is_found
    }
```

---

### 🤖 **[Sandeep Kumar Sahoo](github.com/sandeepsahoo18) – The Broadcaster**

> _Designed the Announcement module APIs with proper access control_

#### 🧩 Features

- 📣 **[Announcement - Fetch By ID](https://github.com/Syllogistek-System/silicon-campus-hub-team-10/blob/lost_found/app/services/announcement.py)**  
  Implemented endpoints to fetch announcements by id.

- 📬 **[Contact](mailto:ece.24becf91@silicon.ac.in)**

🛠️ **How it was done**: A parameterized `GET` endpoint was implemented to retrieve a specific announcement using its unique ID. Upon receiving the request, the system queries the database and returns the corresponding announcement as a structured `JSON` response.

#### 💻 Announcement – Fetch Announcement

```python
@router.get("/admin/announcements/{id}", response_model=announcementOut)
def get_announcement_by_id(id: int, db: Session = Depends(get_db)):
    announcement = db.query(Announcement).filter(Announcement.id == id).first()
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return announcement
```
---

### 🛡️ **[Asmit Raj](https://github.com/AsmitRaj110) –  The Moderator**

> _Handles deletion operations for lost & found items using protected DELETE endpoints. Ensures platform hygiene by validating user roles and request origins before data removal__

#### 🧩 Features

- 🧹 **[Lost & Found - Delete endpoint](https://github.com/Syllogistek-System/silicon-campus-hub-team-10/blob/lost_found/app/services/lost_found.py)**  
  Implemented endpoints to Delete Lost & Found expired data and maintaining clean Data Base.

- 📬 **[Contact](mailto:cse.24bcsi64@silicon.ac.in)**

🛠️ **How it was done**: Role-based access control was enforced via `Depends(get_current_user)`. `SQLAlchemy ORM` was used to locate and remove entries by ID, and custom exceptions were raised for unauthorized or invalid actions.

#### 💻 Delete - Delete Lost and Found data by ID

```python
@router.delete("/{id}/delete", status_code=204)
def delete_lost_found_item(
    id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    lost_item = db.query(LostFoundItem).filter(LostFoundItem.id == id).first()

    if not lost_item:
        raise HTTPException(status_code=404, detail="Lost/Found item not found")

    db.delete(lost_item)
    db.commit()
    return {"message": "Item deleted successfully"}
```
---

### 🔎 **[Ashutosh Das](https://github.com/Ashutosh-Das-web) - The Identifier**

> _Built the endpoint to retrieve a specific lost or found post by its unique ID_

#### 🧩 Features

- 🔍 **[Lost & Found: Fetch By ID](https://github.com/Syllogistek-System/silicon-campus-hub-team-10/blob/lost_found/app/services/lost_found.py)**  
  Built listing and search routes for lost/found items by unique ID.

- 📬 **[Contact](mailto:cse.24bcsf49@silicon.ac.in)**

🛠️ **How it was done**: The `Fetch by ID` feature was implemented using a parameterized GET endpoint in FastAPI. It accepts a unique identifier (id) in the URL path and queries the database using the `ORM` to locate the corresponding Lost & Found record.

```python
@router.get("/lost-found/{id}", response_model=Lost_Found_Out)
def get_lost_found_item_id(id: int, db: Session = Depends(get_db)):
    item = db.query(LostFoundItem).filter(LostFoundItem.id == id).first()

    if item is None:
        raise HTTPException(status_code=404, detail="Lost/Found item not found")

    print(item)
    return item
```

---

### 📜 **[Sikhar Sambhab Mund](https://github.com/Sikhar-Mund) – The Historian**

> _Tasked with designing the endpoint to retrieve the entire Lost & Found database._

#### 🧩 Features

- 🧪 **[Lost & Found: Fetch History](https://github.com/Syllogistek-System/silicon-campus-hub-team-10/blob/lost_found/app/services/lost_found.py)**  
  Built Listing of Lost & Found History.

- 📬 **[Contact](mailto:ece.24becb50@silicon.ac.in)**

🛠️ **How it was done**: The 'GET History of Lost & Found' functionality was developed using a GET endpoint in `FastAPI`. It retrieves all available entries from the databasee. It uses the `ORM` (Object Relational Mapper) to query records from the LostFound model and return them in `JSON` format..

```python

@router.get("/lostfound", response_model=List[Lost_Found_Out])
def list_lost_found_items(db: Session = Depends(get_db)):
    items = db.query(LostFoundItem).order_by(LostFoundItem.created_at.desc()).all()
    return items

```

---

## 🙌 Final Words

> 💙 **Big Thanks** to our mentors and [**Syllogistek Team**](https://github.com/Syllogistek-System) for giving us this incredible opportunity!  
> This project gave us hands-on experience in API design, teamwork, and production-ready development.

> 💡 _We don't just code — we craft solutions._  
> 🚀 **With Gratitude,  
> — The Silicon Campus Hub Team 10**

---
