---

🏠 HouseTech

A Real Estate Management System built with Django, Firebase, Cloudinary, and PostgreSQL


---

📖 Overview

HouseTech is a backend-powered real estate management system built using Django.
It enables property owners and agents to list, manage, and browse real estate properties securely and efficiently.

The system integrates Firebase Authentication for user management, Cloudinary for media storage, Neon PostgreSQL for the database, and is deployed on Render for scalability and continuous delivery.


---

✨ Features

🔐 Authentication & User Management

Secure user authentication 

User-based access control — only authenticated users can manage listings

Ownership rules enforced: users cannot edit or delete properties they don’t own



---

🏡 Property Management

Create, update, and delete property listings

Each listing includes essential details such as title, description, price, address, and images

Properties are stored and managed through Django’s ORM for reliability and efficiency



---

🔍 Filtering & Search

Advanced filtering for properties based on:

Location

Price range

Property type


Supports combined query parameters for refined search results



---

📄 Pagination

Efficient pagination system for listing endpoints

Ensures smooth browsing performance even with large datasets



---

⚙️ Admin Dashboard (Django Admin)

Full-featured Django Admin Panel for managing:

Users

Property listings

Cloudinary media files


Superusers have complete administrative control



---

☁️ Cloud & Database Integrations

Cloudinary for secure cloud-based image and media storage

Neon PostgreSQL for fast, scalable, and serverless database hosting

Render for continuous cloud deployment and hosting



---

🔔 Smart Notifications System (Firebase Cloud Messaging)

Integrated Firebase Cloud Messaging (FCM) for real-time notifications

Users can add their favorite locations (cities or areas of interest)

When a new property is added in one of those locations, the system automatically:

Detects matching listings

Sends a personalized notification to all interested users


Keeps users engaged and informed about properties matching their preferences



---