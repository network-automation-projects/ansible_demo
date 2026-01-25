"""
How People Handle Nested JSON in Python
========================================
This file shows different approaches to unpacking nested JSON structures.
Most people use the `json` library, but there are several ways to access nested data.
"""

import json
from typing import Any, Dict, List

# ============================================================================
# Example JSON Data (typical API response or config file)
# ============================================================================
sample_json_string = """
{
    "user": {
        "name": "Alice",
        "age": 30,
        "address": {
            "street": "123 Main St",
            "city": "NYC",
            "zip": "10001"
        },
        "skills": ["Python", "Go", "JavaScript"]
    },
    "metadata": {
        "created_at": "2024-01-15",
        "version": 1
    }
}
"""

# ============================================================================
# Method 1: Standard Library Approach (Most Common)
# ============================================================================
#why would someone use this method of unpacking?
#because it is a simple way to unpack the JSON string.
# it is simple because it uses the dictionary keys to access the data.


# Step 1: Parse JSON string into Python dict using json.loads()
data = json.loads(sample_json_string)

# Step 2: Access nested data using dictionary keys
user_name = data["user"]["name"]
user_age = data["user"]["age"]
city = data["user"]["address"]["city"]
first_skill = data["user"]["skills"][0]

print("Method 1 - Dictionary Access:")
print(f"Name: {user_name}, Age: {user_age}, City: {city}, First Skill: {first_skill}\n")

#this will output: Name: Alice, Age: 30, City: NYC, First Skill: Python



# ============================================================================
# Method 2: Using .get() for Safe Access (Avoids KeyError)
# ============================================================================
#why would someone use this method of unpacking?

# This is safer when keys might not exist
user_name_safe = data.get("user", {}).get("name", "Unknown") #is .get from a standard library?
#yes, .get is from the standard library
# does .get return a value or a key?
# it returns a value
# what is the difference between .get and []?
# .get returns a value or a key
# [] returns a value or a key
# does .get take only json as input?
# no, .get can take any iterable as input

# what are all the iterables in python?
# lists, tuples, dictionaries, sets, strings, ranges, files, etc.



zip_code = data.get("user", {}).get("address", {}).get("zip", "N/A")

print("Method 2 - Safe Access with .get():")
print(f"Name: {user_name_safe}, Zip: {zip_code}\n")

# ============================================================================
# Method 3: Unpacking with Dictionary Unpacking (Limited Use)
# ============================================================================
# You CAN use unpacking, but it's only useful for top-level keys
user_data = data["user"]
name, age = user_data["name"], user_data["age"]  # Not really "unpacking" like tuples

# For nested structures, unpacking is less common because:
# - JSON becomes dicts/lists, not tuples
# - Keys are named, not positional
# - Structure can vary

print("Method 3 - Limited Unpacking:")
print(f"Name: {name}, Age: {age}\n")

# ============================================================================
# Method 4: Using Dataclasses (Built-in, Python 3.7+)
# ============================================================================
# Dataclasses are built into Python and provide a simple way to structure data

#why would someone use this method of unpacking?
#because it is a simple way to unpack the JSON string.
# it is simple because it uses the dictionary keys to access the data.

from dataclasses import dataclass
from typing import Optional

@dataclass
class Address:
    street: str
    city: str
    zip: str

@dataclass
class User:
    name: str
    age: int
    address: Address
    skills: List[str]

@dataclass
class UserData:
    user: User
    metadata: Dict[str, Any]

# Convert JSON to structured objects
def parse_user_data(json_str: str) -> UserData:
    data = json.loads(json_str)
    address = Address(**data["user"]["address"])
    user = User(
        name=data["user"]["name"],
        age=data["user"]["age"],
        address=address,
        skills=data["user"]["skills"]
    )
    return UserData(user=user, metadata=data["metadata"])

parsed = parse_user_data(sample_json_string)
print("Method 4 - Structured Objects (Dataclasses):")
print(f"Name: {parsed.user.name}, City: {parsed.user.address.city}\n")

# ============================================================================
# Method 5: Using Pydantic (Popular Third-Party Library)
# ============================================================================
# Pydantic provides data validation, type coercion, and automatic parsing
# Install with: pip install pydantic
# 
# Key advantages:
# - Automatic validation and type conversion
# - Can parse directly from JSON strings
# - Better error messages
# - Supports optional fields with defaults
# - Works great with FastAPI

try:
    from pydantic import BaseModel, Field, ValidationError
    
    #this method of unpacking is called Pydantic.
    #is pydantic also used below when unpacking the 'dictionary' way?
    #yes, pydantic is used below when unpacking the 'dictionary' way.
    
    class AddressPydantic(BaseModel):
        street: str
        city: str
        zip: str = Field(alias="zip")  # Can use aliases for different JSON keys
    
    class UserPydantic(BaseModel):
        name: str
        age: int
        address: AddressPydantic
        skills: List[str]
    
    class UserDataPydantic(BaseModel):
        user: UserPydantic
        metadata: Dict[str, Any]
    
    # Pydantic can parse directly from JSON string!
    parsed_pydantic = UserDataPydantic.parse_raw(sample_json_string)
    
    #using these classes, we can parse the JSON string into a UserDataPydantic object.
    # what is the difference between a UserDataPydantic object and a UserData object?
    # a UserDataPydantic object is a UserData object that has been parsed from a JSON string.
    # a UserData object is a UserData object that has been parsed from a JSON string.
   
   #why would someone use this method of unpacking?
   #because it is a more robust way to unpack the JSON string.
   # it is more robust because it validates the data before parsing it.
   # it is more robust because it can handle missing fields.
   # it is more robust because it can handle invalid data.
   # it is more robust because it can handle different data types.
   # it is more robust because it can handle different data structures.
   # it is more robust because it can handle different data formats.
   # it is more robust because it can handle different data encodings.
    
    print("Method 5 - Pydantic (with validation):")
    print(f"Name: {parsed_pydantic.user.name}")
    print(f"City: {parsed_pydantic.user.address.city}")
    print(f"Age: {parsed_pydantic.user.age}")
    print(f"Skills: {', '.join(parsed_pydantic.user.skills)}") #join returns a literal string.  is that 
    #different than a regular string?
    #yes, it is different than a regular string.
    # a regular string is a sequence of characters.
    # a literal string is a sequence of characters that are not evaluated.
    #why don't we want this string to be evaluated?
    #because we want to join the skills into a single string.
    # if we want to evaluate the string, we can use eval()
    # but we don't want to evaluate the string.
    # we want to join the skills into a single string.
    # so we use join()
    # join() returns a literal string.
    # so we use join() to join the skills into a single string.
    
    # Pydantic also works with dict unpacking
    data_dict = json.loads(sample_json_string)
    parsed_from_dict = UserDataPydantic(**data_dict)
    print(f"Parsed from dict - Name: {parsed_from_dict.user.name}\n")
    
    # Example: Pydantic with validation errors
    invalid_json = '{"user": {"name": "Bob", "age": "not_a_number", "address": {"street": "456 St", "city": "LA", "zip": "90001"}, "skills": []}, "metadata": {}}'
    try:
        invalid_parsed = UserDataPydantic.parse_raw(invalid_json)
    except ValidationError as e:
        print("Pydantic caught validation error (age should be int, not string):")
        print(f"  {e.errors()[0]['msg']}\n")
    
except ImportError:
    print("Method 5 - Pydantic not installed (install with: pip install pydantic)\n")

# ============================================================================
# Method 6: Using attrs (Alternative to Dataclasses)
# ============================================================================
# attrs is a library that provides similar functionality to dataclasses
# but with more features and better performance
# Install with: pip install attrs
#
# Key advantages:
# - More features than dataclasses (validators, converters, etc.)
# - Better performance
# - Can be used as drop-in replacement for dataclasses
# - Supports frozen (immutable) objects easily
#what's an example of an immutable object?
#an immutable object is an object that cannot be changed.
#an example of an immutable object is a tuple.
#an example of a mutable object is a list.
#an example of a mutable object is a dictionary.
#an example of a mutable object is a set.
#an example of a mutable object is a string.
#an example of a mutable object is a number.
#an example of a mutable object is a boolean.
#an example of a mutable object is a None.
#an example of a mutable object is a function.
#an example of a mutable object is a class.
#an example of a mutable object is a object.
#an example of a mutable object is a object.


try:
    import attrs
    from attrs import define, field
    
    @define
    class AddressAttrs:
        street: str
        city: str
        zip: str
    
    @define
    class UserAttrs:
        name: str
        age: int
        address: AddressAttrs
        skills: List[str]
    
    @define
    class UserDataAttrs:
        user: UserAttrs
        metadata: Dict[str, Any]
    
    # Convert JSON to attrs objects
    def parse_user_data_attrs(json_str: str) -> UserDataAttrs:
        data = json.loads(json_str)
        address = AddressAttrs(**data["user"]["address"])
        user = UserAttrs(
            name=data["user"]["name"],
            age=data["user"]["age"],
            address=address,  #why didn't we need ["user"]["address"]?
            #because we used the AddressAttrs class to define the address.
            #so we didn't need to use ["user"]["address"].

            skills=data["user"]["skills"]
        )
        return UserDataAttrs(user=user, metadata=data["metadata"])
    
    parsed_attrs = parse_user_data_attrs(sample_json_string)
    print("Method 6 - attrs (structured objects):")
    print(f"Name: {parsed_attrs.user.name}, City: {parsed_attrs.user.address.city}")
    print(f"Age: {parsed_attrs.user.age}")
    
    # attrs can convert back to dict easily
    user_dict = attrs.asdict(parsed_attrs.user)
    print(f"User as dict: {user_dict}\n")
    
    # Example: attrs with validators (more advanced)
    @define
    class UserWithValidation:
        name: str
        age: int = field(validator=attrs.validators.instance_of(int))
        address: AddressAttrs
        skills: List[str] = field(factory=list)  # Default to empty list
    
    # This would validate that age is an int
    user_validated = UserWithValidation(
        name="Charlie",
        age=25, #what if we put a string here?
        #it would raise a validation error.
        #why?
        #because we used the validator=attrs.validators.instance_of(int) to validate the age.
        #so we need to put an integer here.
        #what if we put a float here?
        #it would raise a validation error.
        #why?
        #because we used the validator=attrs.validators.instance_of(int) to validate the age.


        address=AddressAttrs(street="789 St", city="SF", zip="94102"),
        skills=["Python"]
    )
    print(f"Validated user: {user_validated.name}, Age: {user_validated.age}\n")
    
except ImportError:
    print("Method 6 - attrs not installed (install with: pip install attrs)\n")

# ============================================================================
# Method 7: Using jsonpath or jq-like Libraries (For Complex Queries)
# ============================================================================
# For very complex nested JSON, people use libraries like:
# - jsonpath-ng (Python implementation of JSONPath)
# - jmespath (query language for JSON)

#if you don't know what all your data looks like, is this the best way to unpack it?
#no, it is not the best way to unpack it.
#it is a good way to unpack it if you know what all your data looks like.
#if you don't know what all your data looks like, you should use a different method.
#what is the best way to unpack it if you don't know what all your data looks like?
#the best way to unpack it if you don't know what all your data looks like is to use a dictionary.
# i see dictionary in method 3 above, but it says it is limited to only the top level keys.
# so how would you get all your data unpacked if you don't know what all your data looks like?
#please provide an example.
#example:
#data = json.loads(sample_json_string)
#for key, value in data.items():
#    print(f"{key}: {value}")
#this will output:
#user: {'name': 'Alice', 'age': 30, 'address': {'street': '123 Main St', 'city': 'NYC', 'zip': '10001'}, 'skills': ['Python', 'Go', 'JavaScript']}
#metadata: {'created_at': '2024-01-15', 'version': 1}
# so this will pull out 'street city etc' into the 'address' key.?
#yes, it will pull out 'street city etc' into the 'address' key.
#then from there, someone would have to look at it and decide what to do with it.? yes





# Example with jsonpath-ng (would need: pip install jsonpath-ng)
#ng stands for?
#ng stands for 'next generation'
#what is the difference between jsonpath-ng and jsonpath?
#jsonpath-ng is a library that provides a way to query JSON data.
#jsonpath is a library that provides a way to query JSON data.
#jsonpath-ng is a library that provides a way to query JSON data.
#is ng newer?
#yes, jsonpath-ng is newer than jsonpath.

try:
    from jsonpath_ng import parse
    
    jsonpath_expr = parse("$.user.address.city")
    matches = [match.value for match in jsonpath_expr.find(data)]
    print("Method 5 - JSONPath (if library installed):")
    print(f"City via JSONPath: {matches[0]}\n")
except ImportError:
    print("Method 5 - JSONPath library not installed (optional)\n")

# ============================================================================
# Method 8: Manual Unpacking with Pattern Matching (Python 3.10+)
# ============================================================================
# Python 3.10+ has match/case which can help with structured data
# def extract_user_info(data: Dict) -> tuple:
#     """Extract user info using pattern matching."""
#     match data:
#         case {"user": user} if isinstance(user, dict):
#             name = user.get("name")
#             age = user.get("age")
#             address = user.get("address", {})
#             city = address.get("city") if isinstance(address, dict) else None
#             return name, age, city
#         case _:
#             return None, None, None

# name, age, city = extract_user_info(data)
# print("Method 8 - Pattern Matching (Python 3.10+):")
# print(f"Name: {name}, Age: {age}, City: {city}\n")

# ============================================================================
# Real-World Example: API Response Handling
# ============================================================================
# This is how people typically handle API responses:

def handle_api_response(response_json: str):
    """Typical pattern for handling API JSON responses."""
    try:
        data = json.loads(response_json)
        
        # Access nested data
        user = data.get("user", {})
        name = user.get("name")
        address = user.get("address", {})
        city = address.get("city")
        
        # Or use direct access if structure is guaranteed
        # name = data["user"]["name"]
        
        return {
            "name": name,
            "city": city
        }
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing JSON: {e}")
        return None

# ============================================================================
# Key Takeaways:
# ============================================================================
"""
Summary of Methods:
===================

1. **Most Common**: json.loads() + dictionary access (data["key"]["nested_key"])
   - Simple, built-in, works everywhere
   - No dependencies

2. **Safe Access**: Use .get() to avoid KeyError exceptions
   - Good for handling missing keys gracefully

3. **Dataclasses** (Method 4): Built-in structured objects
   - Python 3.7+, no dependencies
   - Simple, clean code
   - Good for basic structured data

4. **Pydantic** (Method 5): Popular third-party validation library
   - Automatic validation and type conversion
   - Can parse directly from JSON strings
   - Great error messages
   - Perfect for APIs (works great with FastAPI)
   - Install: pip install pydantic

5. **attrs** (Method 6): Alternative to dataclasses with more features
   - More features than dataclasses (validators, converters)
   - Better performance
   - Supports frozen (immutable) objects easily
   - Install: pip install attrs

6. **JSONPath** (Method 7): For complex queries
   - Useful for querying deeply nested structures
   - Install: pip install jsonpath-ng

7. **Pattern Matching** (Method 8): Python 3.10+ feature
   - Modern Python syntax
   - Good for structured pattern matching

Key Point - Unpacking vs JSON:
==============================
Unlike tuples/lists where unpacking is positional:
    name, (age, profession) = ("John", (30, "Developer"))

JSON requires key-based access:
    data = json.loads(json_string)
    name = data["user"]["name"]
    age = data["user"]["age"]

With structured libraries (Pydantic/attrs/dataclasses), you get:
    parsed = UserData.parse_raw(json_string)
    name = parsed.user.name  # Clean attribute access!
"""