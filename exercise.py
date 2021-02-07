"""
Exercise 5:
"""

# Create a variable called student, with a dictionary.
# The dictionary must contain three keys: 'name', 'school', and 'grades'.
# The values for each must be 'Jose', 'Computing', and a tuple with the values 66, 77, and 88.
student = {
    'name': 'Jose',
     "school": "Computing",
     'grades': (66,77,88)
}

# Assume the argument, data, is a dictionary.
# Modify the grades variable so it accesses the 'grades' key of the data dictionary.
def average_grade(data):
    grades = data['grades']  # Change this!
    return sum(grades) / len(grades)


# Implement the function below
# Given a list of students (a list of dictionaries), calculate the average grade received on an exam, for the entire class
# You must add all the grades of all the students together
# You must also count how many grades there are in total in the entire list
def average_grade_all_students(student_list):
    total = 0
    count = 0
    for student in student_list:
        total += sum(student['grades'])
        count += len(student['grades'])
    return total / count


"""
Exercise : 6 Classes and objects
"""

class Store:
    def __init__(self,name):
        # You'll need 'name' as an argument to this method.
        # Then, initialise 'self.name' to be the argument, and 'self.items' to be an empty list.
        self.name = name
        self.items = []
    
    def add_item(self, name, price):
        # Create a dictionary with keys name and price, and append that to self.items.
        dic = {'name': name, 'price': price}
        self.items.append(dic) 

    def stock_price(self):
        # Add together all item prices in self.items and return the total.
        total = 0
        for item in self.items:
            total += item['price']

        return total

"""
Exercise : 7 @classmethod and @staticmethod
"""

class Store:
    def __init__(self, name):
        self.name = name
        self.items = []

    def add_item(self, name, price):
        self.items.append({
            'name': name,
            'price': price
        })

    def stock_price(self):
        total = 0
        for item in self.items:
            total += item['price']
        return total

    @classmethod
    def franchise(cls, store):
        # Return another store, with the same name as the argument's name, plus " - franchise"
        return cls(store.name + ' - franchise')

    @staticmethod
    def store_details(store):
        # Return a string representing the argument
        # It should be in the format 'NAME, total stock price: TOTAL'
        return '{}, total stock price: {}'.format(store.name, int(store.stock_price()))

"""
Q - WHAT IS A REST API 
ANS - it's a way of thinking about how to web server responds to your requests, it doesn't respond with just data
it respond with resources. rest api is stateless..

# setup virtual environment for python 3.5+
python -m venv drive:/path/to/directory
## for window
- ./venv/Scripts/activate.bat 

# Heroku?

ans- herku is kind of hosting service it makes available to anybody to interact with your app.
    it provide link for you. it works with dyno which works on virualization..it reads from github..
    so must be deploy first on github

Conclusion :
    -A distributed hosting service 
    -Each server is called a "dyno", and it runs your application
    -Free tier gives you 1 dyno, but limited running hours
"""