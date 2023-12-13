# ARRM - Research Resource Management System

ARRM is a web application designed to facilitate the matching of Research Assistants to faculty members.

## System Architectures

### 1. Three-Tier Architecture

- **Presentation Layer:** Frontend built with React JS, HTML, and CSS.
- **Logic Layer:** Backend powered by the Python Framework, Django.
- **Data Layer:** Database storing information on web application users.

### 2. Model-View-Controller (MVC) Architecture

#### MVC Description:

- **Model Component:** Controls system data and operations, overseeing updates to RA skillsets, project details, and profile information.
- **View Component:** Defines and manages presentation of RA, lecturer, and project data to the user.
- **Controller Component:** Manages user interactions, such as clicking update profile or request RA buttons.

#### Justification for MVC:

- **Reason:** Build a 3-tier architecture with components that can be built iteratively and independently. This allows users to benefit from implemented functionalities while developers make incremental updates to add other features to the platform.

## Frontend Technology: React JS Framework

### Key Features of React JS:

- **Component-Based Architecture:** Develop user interfaces as a collection of reusable components for code reusability, maintenance, and scalability.
- **JSX Support:** Write HTML-like code directly within JavaScript, simplifying code and improving readability.
- **Vast Ecosystem:** Benefit from numerous libraries, tools, and resources within the React ecosystem, with an active community providing support, tutorials, and updates.
- **CSS Integration:** Use CSS for styling React JS components, employing Tailwind CSS and CSS to meet software requirements and functionalities.

## Backend Technology: Django and Django Rest Framework

In developing the Ashesi Research Resource Management System (ARRM), the selection of technology stands as a critical factor influencing the system's robustness, scalability, and maintainability. Embracing the Model-View-Controller (MVC) architecture for effective separation of concerns, our choice centered on Django and Django Rest Framework (DRF), each contributing significantly to distinct aspects of our system.

### Django for Backend Structure and ORM

Django's commitment to the MVC architecture provides a well-organized framework for structuring the backend. The Model component supports the definition of data models and interactions with the database. The Object-Relational Mapping (ORM) system within Django abstracts away the complexities of database management, facilitating seamless communication with various database systems and enhancing development speed.

Moreover, Django's built-in authentication systems, middleware support, and URL routing contribute to a secure and scalable backend structure. The framework's 'batteries-included' philosophy offers numerous utilities and tools, minimizing the reliance on external dependencies and promoting consistency in development.

### Django Rest Framework for API Development

Complementing Django, Django Rest Framework excels in developing robust and RESTful APIs. Leveraging DRF ensures that our Research Resource Management System boasts a flexible and standardized interface for seamless communication between frontend and backend components. DRF's serializers simplify the conversion of complex data types, such as Django models, into Python data types that can be effortlessly rendered into JSON.

DRF's support for authentication classes, permissions, and view sets streamlines access control implementation, ensuring that the API adheres to our system's security requirements. Additionally, DRF's support for various response formats and content negotiation enhances the system's adaptability to client-side technologies.

### Scalability and Community Support

Both Django and DRF benefit from active and vibrant communities. Regular updates, extensive documentation, and a plethora of third-party packages make it easy to find solutions to common problems and stay current with best practices. This, coupled with the scalability inherent in Django's design, ensures that our Research Resource Management System can easily accommodate future enhancements and increased user loads.

## MySQL

MySQL stands as our chosen backend database for its proven reliability and stability, forming a secure foundation for storing critical data in the Ashesi Research Resource Management System. MySQL's scalability is vital as our application grows, providing the capability to handle increased data loads and larger datasets efficiently. The seamless integration of MySQL with the Django framework simplifies development and maintenance processes. Furthermore, MySQL's robust support for transactions (grouping of one or more SQL statements that interact with a database) aligns well with the relational nature of our data, emphasizing data integrity and consistency. Overall, MySQL emerged as a dependable and well-supported choice for our backend database, enhancing the efficiency and performance of our system.

## Postman Collection:
Find the link to the postman collection [here](https://arrm-ashesi.postman.co/workspace/Team-Workspace~8f8d231b-922d-40c2-8a28-e0a1cdc9d842/collection/31703248-139b06bf-29be-47ab-bd12-7b239f21657a?action=share&creator=31703248)
