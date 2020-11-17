from Database import Database
from datetime import date
import sqlite3
# from pprint import pprint

class Post_user:
    def __init__(self, user):
        self.user = user
        self.posts = 0
        self.db = Database()

    def makepost(self):
        makingpost = True
        while makingpost:
            # Collect post information
            title = input('Enter your title: ')
            body = input('Enter the body of your post: ')
            # Make sure user wants to post this
            print(title)
            print(body)
            postcheck = input('Is this what you would like to post? (Y/N)').lower()
            if postcheck[0] == 'y':
                pdate = date.today()
                # need to make some variable in main called posts that counts total posts
                id = str(self.posts).zfill(3)  # fills posts with up to 3 zeros
                self.posts += 1
                pid = 'p' + id
                print(pid)
                self.db.c.execute("""
                INSERT INTO posts VALUES (?, ?, ?, ?, ?)
                """, (pid, pdate, title, body, self.user)
                                )
                self.db.commit()
                print('You have posted "', title, '" to Tidder.')
                makingpost = False
            else:
                print('Post deleted. Please type it again.')
        return pid #returns ID of post being made, for answer() function

    def searchposts(self):
        searching = True
        while searching: # As long as user is willing to search
            print('What would you like to search? Enter any combination of words.')
            entry = input('Enter your search here: ')
            print('Searching...')
            query = entry.split()
            self.db.row_factory = sqlite3.Row  # Might be unnecessary
            for entry in query:
                self.db.c.execute("""
                    SELECT DISTINCT p.pid, p.pdate, p.title, p.body, p.poster, COUNT(vno) as votes, COUNT(a.pid) as answers
                    FROM posts p
                    LEFT JOIN answers a ON a.qid = p.pid
                    LEFT JOIN votes v ON v.pid = p.pid
                    LEFT JOIN tags t ON t.pid = p.pid
                    WHERE p.title LIKE ?
                    OR p.body LIKE ?
                    OR t.tag LIKE ?
                    GROUP BY p.pid; """, ('%'+entry+'%', '%'+entry+'%', '%'+entry+'%')) # why is it displaying 2 answers what the flip
            results = self.db.c.fetchall()
            page = 0
            selecting_post = True
            lim_results = [results[x:x + 5] for x in range(0, len(results), 5)] # Breaks results into groups of 5
            column = self.db.c.description
            while selecting_post:
                # Page decides what page of search results to look at, starts at 0
                try:
                    """Inserts names of columns at beginning of results"""
                    columns = []
                    for name in column: # Takes names of columns out of list
                        columns.append(name[0])
                    inter_columns = tuple(columns) # Turns list into tuple
                    if lim_results != []: # So IndexError still exists if there are no results
                        if lim_results[page][0] != inter_columns: # Only inserts column names once
                            lim_results[page].insert(0, inter_columns)
                    """Prints results according to page, and allows selection"""
                    self.db.print_table(lim_results[page]) # Pretty prints results to console. (USING STOLEN CODE O.O)
                    print('Page', page+1, 'of', len(lim_results))
                    """Had to move selection() to searchposts bc im dumb"""
                    print('To select a post, enter the post ID.')
                    print('To switch pages, type L (left) or R (right).')
                    print('To go back, type back.')
                    select = input('What would you like to do? > ').lower()
                    if select[0] == 'p' and len(select) == 4:
                        post = select
                        # Need to check the post selected is actually in the database
                        self.db.c.execute('SELECT pid FROM posts WHERE pid = ?', (post,))
                        exist = self.db.c.fetchall()
                        if exist:
                            print("\n")
                            self.postaction(post)
                        else:
                            print('The post you have selected does not exist. Please select a post.\n')
                    elif select == 'back':
                        selecting_post = False
                    elif select[0] == 'l':
                        if page >= 0:
                            page -= 1
                        else:
                            print('No more pages to be found.')
                    elif select[0] == 'r':
                        if page <= len(lim_results):
                            page += 1
                    else:
                        print('Invalid input. Try again.')
                except IndexError:
                    print('Sorry, no results found.')
                    selecting_post = False
            ask = input('Would you like to search again? (Y/N)').lower()
            if ask[0] == 'n':
                searching = False


    def answer(self, post):
        pid = self.makepost() # Returns ID of ANSWER post
        try:
            self.db.c.execute("""
            INSERT INTO answers VALUES
            (?, ?) """, (pid, post))
            print('In response to', post + '.', '\n')
        except sqlite3.IntegrityError as e:
            print("Violates our protocol: ", e, '\n')
        except Exception:
            print("Some error occurred. Try again.", '\n')


    def vote(self, post):
        self.db.c.execute('SELECT MAX(vno) FROM votes') # as votes increments by one, this will return the latest vote
        totalvotes = self.db.c.fetchall()

        # Check if user already voted
        vdate = date.today()
        vote = int(totalvotes[0][0]) + 1 # Gets number from list of tuple, as it is formatted like [(number)]
        self.db.c.execute('INSERT INTO votes VALUES (?, ?, ?, ?)', (post, vote, vdate, self.user))
        print('Voted successfully!')
        print('You are vote number', vote, '.\n')

    def postaction(self, post):
        deciding = True
        privilegedUser = self.privileged()

        while deciding: # showing the options to user
            print('To vote on this post, type "v".')
            print('To answer this post, type "a". ')

            if privilegedUser: # only shows when the user is a privileged user
                print('To mark as an acceptable answer for the question of the post,\n'+'   if it is an answer, type "m".')
                print('To give a badge for this post, type "b".')
                print('To give tags on this post, type "t".')
                print('To edit the post, type "edit"')

            print('To go back to search results, type "back".')

            # user choose an option
            action = input('What would you like to do? >').lower()
            if action == 'a':
                self.answer(post)
            elif action == 'v':
                self.vote(post)
            elif action == 'back':
                deciding = False
                self.searchposts()
            elif privilegedUser:
                if action == 'm':
                    self.markAcceptableAnswer(post)
                elif action == 'b':
                    self.giveBadges(post)
                elif action == 't':
                    self.giveTags(post)
                elif action == 'edit':
                    self.editPost(post)
                else:
                    print('Invalid action. Please try again.')
            else:
                print('Invalid action. Please try again.')


    def markAcceptableAnswer(self, post):
        """
        The post can have multiple situations while marking.
        1. the question of the post already has a accepted answer
            find the question from the post(answer)
            check if the question has any accepted answer
                if it has, then update
                if error, then print error message
        2. the question does not have any accepted answer
            insert the qid, post into the questions database
        :param post: the answer that we care about
        :return: error message / update acceptable answer/ insert acceptable answer (if not present)
        """
        # check if the post is an answer
        self.db.c.execute('SELECT * FROM answers WHERE pid = ?;', (post,))
        answer = self.db.c.fetchall() # should be zero if it is a question
        if not answer:
            print("Questions cannot be marked as accepted answers. Search again\n")
            self.searchposts()

        # Getting the question id using the answer post
        self.db.c.execute('SELECT qid FROM answers WHERE pid = ?;', (post,))
        questionid = self.db.c.fetchall()

        # Getting the accepted answer for this question (if any)
        self.db.c.execute('SELECT theaid FROM questions WHERE pid = ?;', (questionid[0][0],))
        markedAnswer = self.db.c.fetchall() # # markedAnswer is an empty list if the post is still not marked

        print("\n")
        print("The question of the current selected answer:")
        self.db.c.execute('SELECT * FROM posts WHERE pid = ?;', (questionid[0][0],))
        results = self.db.c.fetchall()
        self.printTable(results)
        self.db.commit()

        if markedAnswer:
            # the question of the post already has a accepted answer
            print("The current accepted answer: ")
            self.db.c.execute('SELECT * FROM posts WHERE pid = ?;', (markedAnswer[0][0],))
            results = self.db.c.fetchall()
            self.printTable(results)

            print("The answer you selected:")
            self.db.c.execute('SELECT * FROM posts WHERE pid = ?;', (post,))
            results = self.db.c.fetchall()
            self.printTable(results)
            self.db.commit()

            print('The question already has an accepted answer. Do you want to change it? (Y/N)')
            ask = self.replyYesNo()

            if ask:
                try:
                    self.db.c.execute("""UPDATE questions SET theaid = ? WHERE pid = ?;""", (post, questionid[0][0]))
                    print("Acccepted answer has been updated to: ", post)
                except Exception:
                    print("Error occurred. Please try again later.")
                print("\n")
                self.db.commit()
                self.postaction(post)

            else: # user cancelled
                print("Operation Cancelled")
                print("\n")
                self.postaction(post)

        elif not markedAnswer:  # does not have any selected answer
            print("The answer you selected:")
            self.db.c.execute('SELECT * FROM posts WHERE pid = ?;', (post,))
            results = self.db.c.fetchall()
            self.printTable(results)
            self.db.commit()
            print("Are you sure you want to make the changes?")
            ask = self.replyYesNo()

            if ask:
                try:
                    self.db.c.execute("""INSERT INTO questions VALUES (?, ?);""", (questionid[0][0], post))
                    print("Accepted answer has been updated to: ", post)
                    self.db.commit()
                except Exception:
                    print("Error occurred. Please try again later.")
                print("\n")
                self.postaction(post)

            else: # user cancelled
                print("Operation Cancelled")
                print("\n")
                self.postaction(post)

        else:
            print("Unknown error occurred. Please try again later.")

    def replyYesNo(self):
        key = True
        ask = ''
        while key:
            ask = input().lower()

            if ask == 'y' or ask == 'yes':
                key = False
                return True
            elif ask == 'n' or ask == 'no':
                key = False
                return False
            else:
                print('Invalid response, please select (Y/N)')
                continue

    def printTable(self, results):
        """
        Prints the table with rows in results
        :param results: rows
        :return: prints the rows
        """
        try:
            self.db.print_table(results)  # Pretty prints results to console. (USING STOLEN CODE O.O)
        except IndexError:
            print('Sorry, no results found.')

    def giveBadges(self, post):
        """
        Privileged user can give badges to posts they like, when they select a post, they can write the badge
        name that they want to give. If the badge is in our system, then update ubadges database with all
        the necessary information but if it is not, give an error message and return the user back to
        selection page.
        :param post: the post selected
        :return: (for successful attempt), ubadges is updated with the badge
        """
        print("What badge would you like to give this post?")
        badge = input()

        # Check if the badge is present in our system.
        self.db.c.execute("""SELECT *
                             FROM badges
                             WHERE bname = ?;""", (badge,))
        badgeInSystem = self.db.c.fetchall()

        if badgeInSystem:   # not an empty list
            # update ubadges
            try:
                self.db.c.execute("""
                                INSERT INTO ubadges VALUES
                                (?, ?, ?);  
                                """, (self.user, date.today(), badge))
                print("working on it...")
                print("You gave a badge! Thanks for reviewing")
                self.db.commit()
                # return user back to postaction page.
                print("\n")  # for clarity
                self.postaction(post)
            except sqlite3.IntegrityError as e: # if duplicate data
                print("This data already exists. Returning back to action page.\n")
                self.postaction(post)
            except Exception: # for any other problem
                print("Something went wrong. Please try again.\n")
                self.giveBadges(post)

        else:  # empty list, badge not present
            print("Sorry, the badge is not in our system. Try again? (Y/N)")
            answer = self.replyYesNo()

            if answer:  # user wants to try again
                self.giveBadges(post)
            else:  # user gave up
                print("\n")  # for clarity
                self.postaction(post)

    def giveTags(self, post):
        """
        privileged user can give tags to any posts that they have selected. And tags can be more than 1 or
        take all the tags in, makes sure the tags are unique (case insensitive). Then update in the database.
        :param post: the post selected
        :return: updates information to database and print confirmation
        """
        tags = []
        index = 1
        inputValue = ''

        # Taking in user tags
        print("Write 'end' when you are done with tags")
        while inputValue != 'end':
            print("Tag ", index, ":")
            inputValue = input()
            inputValue = inputValue.lower()

            tags.append(inputValue)
            index = index + 1

        tags.remove("end")      # "end" is not part of tag
        tags = list(set(tags))  # keeping only unique values
        print("working on it...")
        if tags:
            # inserting all the tags in database
            for i in range(len(tags)):
                try:
                    self.db.c.execute("""INSERT OR IGNORE INTO tags VALUES
                                         (?, ?);
                                      """, (post, tags[i]))
                    self.db.commit()

                # for any error while inserting values in database
                except Exception as e:
                    print("Something went wrong, please try again. Exception: \n", e)
                    self.giveTags(post)

            # Operation done
            print("Tags for this post has been updated.")
            print("\n")  # for clarity
            self.postaction(post)
        else: # If user press "end" without giving any input
            print("Operation Cancelled")
            print("\n")  # for clarity
            self.postaction(post)

    def editPost(self, post):
        """
        editPost takes a the post that user selected and gives the option to edit the title and/or the body
        of the post.
        :param post: the post selected
        :return: update the title and/or body of the post, and output confirmation.
        """
        print("If you do not want to change a part of the post, press enter to skip")
        print("What do you want the new title to be?")
        title = input()
        print("Update new description")
        body = input()

        if title == '' and body == '':  # If the user do not provide any info
            print("Nothing to update. Do you want to perform any other operations?")
            print("\n")  # for clarity
            self.postaction(post)
        elif body == '': # user only wants to change the title
            try:
                self.db.c.execute("""
                                    UPDATE posts
                                    SET title = ?
                                    WHERE pid = ?;
                                  """, (title, post))
                print("working on it...")
                print("The title of the post is updated.")
                print("\n")  # for clarity
                self.postaction(post)
            except Exception as e:
                print("Unknown error occurred. Please try again. Exception: \n", e)
                self.editPost(post)
        elif title == '':  # user only wants to change the body
            try:
                self.db.c.execute("""
                                    UPDATE posts
                                    SET body = ?
                                    WHERE pid = ?;
                                  """, (body, post))
                print("working on it...")
                print("The description of the post is updated.")
                print("\n")  # for clarity
                self.postaction(post)
            except Exception as e:
                print("Unknown error occurred. Please try again. Exception: \n", e)
                self.editPost(post)
        else: # user wants to change both
            try:
                self.db.c.execute("""
                                    UPDATE posts
                                    SET title = ?, body = ?
                                    WHERE pid = ?;
                                  """, (title, body, post))
                print("working on it...")
                print("The title and description of the post is updated.")
                print("\n")  # for clarity
                self.postaction(post)
            except Exception as e:
                print("Unknown error occurred. Please try again. Exception: \n", e)
                self.editPost(post)


    def privileged(self):
        """
        Check if user if a privileged user or not.
        :return: True if privileged,
                 False otherwise.
        """
        self.db.c.execute('Select * from privileged;')
        allUserId = self.db.c.fetchall()
        for users in allUserId:
            for user in users:
                if user == self.user:
                    return True

        return False
