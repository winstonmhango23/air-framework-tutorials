# Part 4: Forms and Validation in the Air Framework

Welcome back to our series on the Air web framework! I'm Winston Mhango, and in this fourth installment, we're diving deep into one of the most critical aspects of web development: **forms and validation**.

In our previous posts, we've explored [the basics of Air](01-introduction-to-air-framework.md), [mastered Air Tags](02-mastering-air-tags.md), and learned about [routing and HTTP methods](03-routing-and-http-methods.md). Now it's time to understand how Air handles one of the most common ways users interact with web applications: forms.

## Understanding Forms in Air

Forms are the primary method for collecting user input in web applications. Air provides several approaches for creating, handling, and validating forms, leveraging both its Air Tags system and Pydantic's powerful validation capabilities.

## Creating HTML Forms with Air Tags

Let's start by creating basic HTML forms using Air Tags:

```python
import air

app = air.Air()

@app.page
def contact_page():
    return air.layouts.mvpcss(
        air.H1("Contact Us"),
        air.Form(
            air.Fieldset(
                air.Legend("Personal Information"),
                air.Label("Name:", for_="name"),
                air.Input(type="text", id="name", name="name", required=True),
                
                air.Label("Email:", for_="email"),
                air.Input(type="email", id="email", name="email", required=True),
                
                air.Label("Phone:", for_="phone"),
                air.Input(type="tel", id="phone", name="phone")
            ),
            air.Fieldset(
                air.Legend("Message"),
                air.Label("Subject:", for_="subject"),
                air.Select(
                    air.Option("General Inquiry", value="general"),
                    air.Option("Support Request", value="support"),
                    air.Option("Feedback", value="feedback"),
                    id="subject",
                    name="subject"
                ),
                
                air.Label("Message:", for_="message"),
                air.Textarea(id="message", name="message", rows=5, required=True),
                
                air.Label(
                    air.Input(type="checkbox", id="newsletter", name="newsletter"),
                    "Subscribe to newsletter",
                    for_="newsletter"
                )
            ),
            air.Button("Submit", type="submit"),
            method="POST",
            action="/contact"
        )
    )
```

## Handling Form Submissions

To handle form submissions, we create POST routes that process the form data:

```python
@app.post("/contact")
async def contact_handler(request: air.Request):
    # Extract form data
    form_data = await request.form()
    
    # Access individual fields
    name = form_data.get("name")
    email = form_data.get("email")
    phone = form_data.get("phone")
    subject = form_data.get("subject")
    message = form_data.get("message")
    newsletter = form_data.get("newsletter")
    
    # Process the data (save to database, send email, etc.)
    # ...
    
    # Return a response
    return air.layouts.mvpcss(
        air.H1("Thank You!"),
        air.P(f"Thanks for your message, {name}! We'll get back to you soon.")
    )
```

## Form Validation with Pydantic

While basic form handling is useful, real-world applications require robust validation. Air leverages Pydantic, the same validation library used by FastAPI, to provide powerful form validation:

```python
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class ContactModel(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    phone: Optional[str] = Field(None, pattern=r'^\+?1?\d{9,15}$')
    subject: str = Field(..., pattern=r'^(general|support|feedback)$')
    message: str = Field(min_length=10, max_length=1000)
    newsletter: bool = False

@app.post("/contact")
async def contact_handler(request: air.Request):
    form_data = await request.form()
    
    # Convert form data to dictionary
    data = dict(form_data)
    
    try:
        # Validate the data using Pydantic
        contact = ContactModel(**data)
        
        # Process valid data
        # ...
        
        return air.layouts.mvpcss(
            air.H1("Thank You!"),
            air.P(f"Thanks for your message, {contact.name}!")
        )
    except Exception as e:
        # Handle validation errors
        return air.layouts.mvpcss(
            air.H1("Validation Error"),
            air.P("Please check your input and try again."),
            air.Ul(*[air.Li(str(error)) for error in e.errors()])
        )
```

## The AirForm Class

Air provides a specialized `AirForm` class that combines form rendering with Pydantic validation:

```python
from pydantic import BaseModel, Field, EmailStr
import air

class ContactModel(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    subject: str = Field(..., pattern=r'^(general|support|feedback)$')
    message: str = Field(min_length=10, max_length=1000)

class ContactForm(air.AirForm):
    model = ContactModel

app = air.Air()

@app.page
def contact_page():
    # Create an instance of the form
    form = ContactForm()
    
    return air.layouts.mvpcss(
        air.H1("Contact Us"),
        air.Form(
            form.render(),  # Render the form based on the model
            air.Button("Submit", type="submit"),
            method="POST",
            action="/contact"
        )
    )

@app.post("/contact")
async def contact_handler(request: air.Request):
    # Create form instance from request data
    form = await ContactForm.from_request(request)
    
    if form.is_valid:
        # Access validated data
        contact_data = form.data
        
        # Process the data
        # ...
        
        return air.layouts.mvpcss(
            air.H1("Thank You!"),
            air.P(f"Thanks for your message, {contact_data.name}!")
        )
    else:
        # Display validation errors
        error_list = air.Ul(
            *[air.Li(str(error)) for error in form.errors]
        )
        
        return air.layouts.mvpcss(
            air.H1("Validation Error"),
            air.P("Please correct the following errors:"),
            error_list,
            air.Form(
                ContactForm().render_with_data(dict(await request.form())),
                air.Button("Submit", type="submit"),
                method="POST",
                action="/contact"
            )
        )
```

## Advanced Form Validation

### Custom Validation Methods

You can add custom validation methods to your Pydantic models:

```python
from pydantic import BaseModel, Field, EmailStr, validator
from datetime import datetime

class EventRegistrationModel(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    birth_date: str
    event_date: str
    
    @validator('birth_date')
    def validate_birth_date(cls, v):
        try:
            birth_date = datetime.strptime(v, '%Y-%m-%d')
            if birth_date > datetime.now():
                raise ValueError('Birth date cannot be in the future')
            return v
        except ValueError:
            raise ValueError('Invalid date format. Use YYYY-MM-DD')
    
    @validator('event_date')
    def validate_event_date(cls, v, values):
        try:
            event_date = datetime.strptime(v, '%Y-%m-%d')
            if 'birth_date' in values:
                birth_date = datetime.strptime(values['birth_date'], '%Y-%m-%d')
                age_at_event = (event_date - birth_date).days / 365.25
                if age_at_event < 18:
                    raise ValueError('Must be 18 or older to attend')
            return v
        except ValueError as e:
            raise e
        except Exception:
            raise ValueError('Invalid date format. Use YYYY-MM-DD')
```

### Field Constraints

Pydantic provides numerous field constraints for validation:

```python
from pydantic import BaseModel, Field
from typing import Optional

class ProductModel(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    price: float = Field(gt=0, le=10000)
    quantity: int = Field(ge=0, le=1000)
    description: Optional[str] = Field(None, max_length=1000)
    category: str = Field(..., pattern=r'^(electronics|clothing|books|home)$')
    sku: str = Field(..., min_length=5, max_length=20, pattern=r'^[A-Z0-9-]+$')
```

## Working with Different Form Types

### File Upload Forms

Handling file uploads requires special consideration:

```python
@app.page
def upload_page():
    return air.layouts.mvpcss(
        air.H1("Upload File"),
        air.Form(
            air.Label("Select file:", for_="file"),
            air.Input(type="file", id="file", name="file", accept="image/*"),
            air.Button("Upload", type="submit"),
            method="POST",
            action="/upload",
            enctype="multipart/form-data"
        )
    )

@app.post("/upload")
async def upload_handler(request: air.Request):
    form_data = await request.form()
    uploaded_file = form_data.get("file")
    
    if uploaded_file and uploaded_file.filename:
        # Process the uploaded file
        # Save to disk, database, or cloud storage
        # ...
        
        return air.layouts.mvpcss(
            air.H1("Upload Successful"),
            air.P(f"File {uploaded_file.filename} uploaded successfully!")
        )
    
    return air.layouts.mvpcss(
        air.H1("Upload Failed"),
        air.P("Please select a file to upload.")
    )
```

### Multi-Select and Checkbox Forms

Handling multiple values from checkboxes and multi-select elements:

``python
@app.page
def preferences_page():
    return air.layouts.mvpcss(
        air.H1("Preferences"),
        air.Form(
            air.Fieldset(
                air.Legend("Interests"),
                air.Label(
                    air.Input(type="checkbox", name="interests", value="sports"),
                    "Sports",
                    for_="sports"
                ),
                air.Label(
                    air.Input(type="checkbox", name="interests", value="music"),
                    "Music",
                    for_="music"
                ),
                air.Label(
                    air.Input(type="checkbox", name="interests", value="technology"),
                    "Technology",
                    for_="technology"
                )
            ),
            air.Fieldset(
                air.Legend("Newsletter Frequency"),
                air.Select(
                    air.Option("Daily", value="daily"),
                    air.Option("Weekly", value="weekly"),
                    air.Option("Monthly", value="monthly"),
                    name="frequency"
                )
            ),
            air.Button("Save Preferences", type="submit"),
            method="POST",
            action="/preferences"
        )
    )

@app.post("/preferences")
async def preferences_handler(request: air.Request):
    form_data = await request.form()
    
    # For checkboxes with the same name, we get a list
    interests = form_data.getlist("interests")
    frequency = form_data.get("frequency")
    
    # Process preferences
    # ...
    
    return air.layouts.mvpcss(
        air.H1("Preferences Saved"),
        air.P(f"Interests: {', '.join(interests)}"),
        air.P(f"Frequency: {frequency}")
    )
```

## Form Rendering Customization

The `AirForm` class allows for customization of how forms are rendered:

```python
class CustomContactForm(air.AirForm):
    model = ContactModel
    
    def render_field(self, field_name: str, field_info):
        # Custom rendering for each field
        label = air.Label(field_info.title or field_name.replace('_', ' ').title(), for_=field_name)
        input_element = air.Input(
            type="text",
            id=field_name,
            name=field_name,
            **self.get_field_attributes(field_name)
        )
        return air.Div(label, input_element, class_="form-group")

# Usage
@app.page
def custom_contact_page():
    form = CustomContactForm()
    return air.layouts.mvpcss(
        air.H1("Custom Contact Form"),
        air.Form(
            *[form.render_field(name, field) for name, field in form.model.model_fields.items()],
            air.Button("Submit", type="submit"),
            method="POST",
            action="/custom-contact"
        )
    )
```

## Error Handling and User Feedback

Providing clear error messages is crucial for a good user experience:

```python
@app.post("/contact")
async def contact_handler(request: air.Request):
    form_data = await request.form()
    form = await ContactForm.from_request(request)
    
    if form.is_valid:
        # Process valid data
        return air.RedirectResponse("/thank-you", status_code=303)
    else:
        # Display form with errors
        error_messages = {}
        for error in form.errors:
            field = error['loc'][0] if error['loc'] else 'general'
            if field not in error_messages:
                error_messages[field] = []
            error_messages[field].append(error['msg'])
        
        # Render form with error messages
        return air.layouts.mvpcss(
            air.H1("Contact Us"),
            air.P("Please correct the errors below:", class_="error-summary"),
            air.Form(
                # Render fields with error messages
                *[air.Div(
                    air.Label(field.replace('_', ' ').title(), for_=field),
                    air.Input(
                        type="text",
                        id=field,
                        name=field,
                        value=form_data.get(field, ''),
                        class_="error" if field in error_messages else ""
                    ),
                    air.Ul(*[air.Li(msg, class_="error-message") for msg in error_messages.get(field, [])])
                ) for field in ['name', 'email', 'subject', 'message']],
                air.Button("Submit", type="submit"),
                method="POST",
                action="/contact"
            )
        )
```

## Practical Example: User Registration System

Let's put everything together with a comprehensive user registration example:

```python
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
import hashlib
import air

class UserRegistrationModel(BaseModel):
    username: str = Field(min_length=3, max_length=30, pattern=r'^[a-zA-Z0-9_]+$')
    email: EmailStr
    password: str = Field(min_length=8)
    confirm_password: str
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    age: int = Field(ge=13, le=120)
    
    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

class UserRegistrationForm(air.AirForm):
    model = UserRegistrationModel

app = air.Air()

@app.page
def register_page():
    form = UserRegistrationForm()
    return air.layouts.mvpcss(
        air.H1("Create Account"),
        air.Form(
            air.Fieldset(
                air.Legend("Account Information"),
                air.Label("Username:", for_="username"),
                air.Input(type="text", id="username", name="username", required=True),
                
                air.Label("Email:", for_="email"),
                air.Input(type="email", id="email", name="email", required=True),
                
                air.Label("Password:", for_="password"),
                air.Input(type="password", id="password", name="password", required=True),
                
                air.Label("Confirm Password:", for_="confirm_password"),
                air.Input(type="password", id="confirm_password", name="confirm_password", required=True)
            ),
            air.Fieldset(
                air.Legend("Personal Information"),
                air.Label("First Name:", for_="first_name"),
                air.Input(type="text", id="first_name", name="first_name", required=True),
                
                air.Label("Last Name:", for_="last_name"),
                air.Input(type="text", id="last_name", name="last_name", required=True),
                
                air.Label("Age:", for_="age"),
                air.Input(type="number", id="age", name="age", min=13, max=120, required=True)
            ),
            air.Button("Create Account", type="submit"),
            method="POST",
            action="/register"
        )
    )

@app.post("/register")
async def register_handler(request: air.Request):
    form = await UserRegistrationForm.from_request(request)
    
    if form.is_valid:
        user_data = form.data
        
        # Hash password before storing
        hashed_password = hashlib.sha256(user_data.password.encode()).hexdigest()
        
        # In a real application, you would save to a database here
        # save_user_to_database(user_data.username, user_data.email, hashed_password, ...)
        
        return air.layouts.mvpcss(
            air.H1("Registration Successful!"),
            air.P(f"Welcome, {user_data.first_name}! Your account has been created."),
            air.A("Go to Login", href="/login")
        )
    else:
        form_data = dict(await request.form())
        
        # Create error messages
        error_dict = {}
        for error in form.errors:
            field = error['loc'][0] if error['loc'] else 'general'
            if field not in error_dict:
                error_dict[field] = []
            error_dict[field].append(error['msg'])
        
        # Render form with errors
        return air.layouts.mvpcss(
            air.H1("Create Account"),
            air.P("Please correct the errors below:", class_="error"),
            air.Form(
                air.Fieldset(
                    air.Legend("Account Information"),
                    air.Label("Username:", for_="username"),
                    air.Input(
                        type="text", 
                        id="username", 
                        name="username", 
                        value=form_data.get('username', ''),
                        class_="error" if 'username' in error_dict else ""
                    ),
                    air.Ul(*[air.Li(msg) for msg in error_dict.get('username', [])]),
                    
                    air.Label("Email:", for_="email"),
                    air.Input(
                        type="email", 
                        id="email", 
                        name="email", 
                        value=form_data.get('email', ''),
                        class_="error" if 'email' in error_dict else ""
                    ),
                    air.Ul(*[air.Li(msg) for msg in error_dict.get('email', [])]),
                    
                    air.Label("Password:", for_="password"),
                    air.Input(
                        type="password", 
                        id="password", 
                        name="password",
                        class_="error" if 'password' in error_dict else ""
                    ),
                    air.Ul(*[air.Li(msg) for msg in error_dict.get('password', [])]),
                    
                    air.Label("Confirm Password:", for_="confirm_password"),
                    air.Input(
                        type="password", 
                        id="confirm_password", 
                        name="confirm_password",
                        class_="error" if 'confirm_password' in error_dict else ""
                    ),
                    air.Ul(*[air.Li(msg) for msg in error_dict.get('confirm_password', [])])
                ),
                air.Fieldset(
                    air.Legend("Personal Information"),
                    air.Label("First Name:", for_="first_name"),
                    air.Input(
                        type="text", 
                        id="first_name", 
                        name="first_name", 
                        value=form_data.get('first_name', ''),
                        class_="error" if 'first_name' in error_dict else ""
                    ),
                    air.Ul(*[air.Li(msg) for msg in error_dict.get('first_name', [])]),
                    
                    air.Label("Last Name:", for_="last_name"),
                    air.Input(
                        type="text", 
                        id="last_name", 
                        name="last_name", 
                        value=form_data.get('last_name', ''),
                        class_="error" if 'last_name' in error_dict else ""
                    ),
                    air.Ul(*[air.Li(msg) for msg in error_dict.get('last_name', [])]),
                    
                    air.Label("Age:", for_="age"),
                    air.Input(
                        type="number", 
                        id="age", 
                        name="age", 
                        value=form_data.get('age', ''),
                        min=13, 
                        max=120,
                        class_="error" if 'age' in error_dict else ""
                    ),
                    air.Ul(*[air.Li(msg) for msg in error_dict.get('age', [])])
                ),
                air.Button("Create Account", type="submit"),
                method="POST",
                action="/register"
            )
        )

@app.page
def login_page():
    return air.layouts.mvpcss(
        air.H1("Login"),
        air.Form(
            air.Label("Username:", for_="username"),
            air.Input(type="text", id="username", name="username", required=True),
            
            air.Label("Password:", for_="password"),
            air.Input(type="password", id="password", name="password", required=True),
            
            air.Button("Login", type="submit"),
            method="POST",
            action="/login"
        )
    )

@app.post("/login")
async def login_handler(request: air.Request):
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")
    
    # In a real application, you would verify credentials against a database
    # user = verify_user_credentials(username, password)
    
    # For this example, we'll just simulate a successful login
    if username and password:
        return air.layouts.mvpcss(
            air.H1("Login Successful!"),
            air.P(f"Welcome back, {username}!"),
            air.A("Go to Dashboard", href="/dashboard")
        )
    else:
        return air.layouts.mvpcss(
            air.H1("Login Failed"),
            air.P("Invalid username or password."),
            air.A("Try Again", href="/login")
        )
```

## Best Practices for Forms and Validation

### 1. Always Validate on the Server Side

Never rely solely on client-side validation:

```python
# Good - Server-side validation
@app.post("/contact")
async def contact_handler(request: air.Request):
    form_data = await request.form()
    # Always validate on the server side
    try:
        contact = ContactModel(**dict(form_data))
        # Process valid data
    except Exception as e:
        # Handle validation errors
        pass
```

### 2. Provide Clear Error Messages

```python
# Good - Clear, specific error messages
class UserModel(BaseModel):
    username: str = Field(
        ..., 
        min_length=3, 
        max_length=30,
        description="Username must be 3-30 characters long"
    )
    email: EmailStr = Field(..., description="Must be a valid email address")
```

### 3. Preserve User Input on Errors

```python
# Good - Preserve user input when showing errors
@app.post("/register")
async def register_handler(request: air.Request):
    form_data = await request.form()
    # If validation fails, re-render form with user's input
    return air.layouts.mvpcss(
        air.Form(
            air.Input(
                type="text", 
                name="username", 
                value=form_data.get("username", "")
            )
            # ... other fields
        )
    )
```

### 4. Use Appropriate Input Types

```python
# Good - Use appropriate input types for better UX
air.Input(type="email", name="email")      # Email validation
air.Input(type="tel", name="phone")        # Mobile keyboard
air.Input(type="number", name="age")       # Numeric keyboard
air.Input(type="date", name="birth_date")  # Date picker
```

## What's Coming Next

In our next post, we'll explore templates and Jinja integration, covering:

1. Setting up JinjaRenderer
2. Creating and organizing templates
3. Passing context data to templates
4. Combining Jinja templates with Air Tags
5. Template inheritance and reusable components

## Conclusion

Forms and validation are essential components of any web application, and Air provides powerful tools to handle them effectively. By combining Air Tags for form creation with Pydantic for validation, Air offers a robust yet flexible approach to handling user input.

Key takeaways from this post:

1. Air Tags make it easy to create HTML forms programmatically
2. Pydantic provides powerful server-side validation
3. The `AirForm` class bridges form rendering and validation
4. Proper error handling improves user experience
5. Always validate on the server side, regardless of client-side validation

With forms and validation mastered, you're well-equipped to build interactive web applications with Air. The combination of Air's Python-based approach to HTML generation and Pydantic's validation capabilities makes form handling both powerful and intuitive.

Ready to continue your journey with Air? Make sure to follow this series on [codetips.blog](https://codetips.blog/series) for weekly updates. You can also connect with me through [LinkedIn](https://www.linkedin.com/in/winston-mhango-401980ab/), [GitHub](https://github.com/winstonmhango23/), or by email at winstonmhango23@gmail.com.

See you in the next post where we'll dive into templates and Jinja integration!

---

*This post is part of the "Mastering the Air Framework" series. Stay tuned for more deep dives into this exciting new Python web framework!*
*Previous: [Routing and HTTP Methods](03-routing-and-http-methods.md)*

## Quiz: Test Your Knowledge

1. What class does Air provide for form validation that's built on Pydantic?
   a) AirValidator
   b) AirForm
   c) AirModel
   d) AirSchema

2. Which Pydantic feature is used to define validation rules for form fields in Air?
   a) Validators
   b) Fields
   c) Models
   d) Schemas

3. How do you access form data in an Air route handler?
   a) request.data()
   b) request.form()
   c) request.body()
   d) request.json()

4. True or False: Client-side validation is sufficient for securing web forms, so server-side validation is optional in Air.

5. True or False: Air Forms can automatically render validation errors in the HTML form.

6. Explain the difference between client-side and server-side validation in the context of Air forms, and why both are important.

### Answers:
1. b) AirForm
2. b) Fields
3. b) request.form()
4. False - Client-side validation improves user experience but server-side validation is essential for security
5. True
6. Client-side validation provides immediate feedback to users and reduces server load by catching obvious errors before submission. Server-side validation is crucial for security as it cannot be bypassed by malicious users. Air leverages both: client-side validation through HTML5 attributes and JavaScript, and server-side validation through Pydantic models in AirForm.