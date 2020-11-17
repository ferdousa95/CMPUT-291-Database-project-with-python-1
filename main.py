from user_login import user_login
from Database import Database
from post_operations import Post_user

def main():
    db = Database()
    db.fill_db() # populates database with sample data if present
    running = True
    while running:
        user = user_login() # Creates account or logs user in, and returns user ID

        post = Post_user(user) # Sets the actions on posts to be by the user
        navigating = True
        while navigating: # Gives users
            print('\nWhat would you like to do?')
            print('To make a post, type "mp".')
            print('To search all posts, type "search". ')
            print('To exit the program, type "exit".')
            navigation = input('To log out, type "logout". >').lower()
            if navigation == 'search':
                print("\n")
                post.searchposts()
            elif navigation == 'mp':
                print("\n")
                post.makepost()
            elif navigation == 'logout':
                print('You will now be logged out of tidder.\n')
                navigating = False
            elif navigation == 'exit':
                navigating = False
                running = False
            else:
                print('Invalid input. Please try again.\n')




if __name__ == '__main__':
    main()
