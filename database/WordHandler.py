from AzureConnect import AzureConnect
from connecting import Connecting

class WordHandler:
    def __init__(self):
        self.azure_database = AzureConnect()
        self.conn = self.azure_database.get_connection()
        self.cursor = self.conn.cursor()

    # <--- WORDS TABLE ---> #

    def add_word(self, native, translation):
        try:
            if self.get_word(native, cursor=self.cursor):
                return "word exists"
            else:
                self.cursor.execute('INSERT INTO words (native, translation) VALUES (?, ?)', (native, translation))
        finally:
            self.conn.commit()

    def get_word(self, native, cursor=None):
        try:
            self.cursor.execute('SELECT * FROM words WHERE native = ?', (native,))
            return self.cursor.fetchone()
        finally:
            self.conn.commit()

    def update_progress(self, native):
        try:
            self.cursor.execute('SELECT progress FROM words WHERE native = ?', (native,))
            result = self.cursor.fetchone()
            if result:
                current_progress = result[0]
                new_progress = current_progress + 1

                self.cursor.execute('UPDATE words SET progress = ?, status = ? WHERE native = ?',
                               (new_progress, 'in progress' if new_progress < 10 else 'mastered', native))
        finally:
            self.conn.commit()

    def delete_word(self, native):
        try:
            self.cursor.execute('DELETE FROM words WHERE native = ?', (native,))
            print(f"{native} deleted from database.")
        finally:
            self.conn.commit()

    def get_all(self):
        try:
            self.cursor.execute('SELECT * FROM words')
            return self.cursor.fetchall()
        finally:
            print("got everything")

    def get_finished(self):
        try:
            self.cursor.execute('SELECT * FROM words WHERE progress >= 10')
            return self.cursor.fetchall()
        finally:
            print("got finished")

    def get_unfinished(self):
        try:
            self.cursor.execute('SELECT * FROM words WHERE progress < 10')
            return self.cursor.fetchall()
        finally:
            print("got unfinished")

    def random_element(self):
        try:
            self.cursor.execute('SELECT TOP 1 * FROM words WHERE progress < 10 ORDER BY NEWID()')
            element = self.cursor.fetchone()
            return element
        except Exception as e:
            print(f"Failed to get random element: {e}")


    def add_sentence(self, native, sentence):
        try:
            self.cursor.execute('UPDATE words SET sentence = ?, WHERE native = ?',
                           (sentence, native))
        finally:
            self.conn.commit()
    
    # <--- RECENTLY TRAINED TABLE ---> #

    def add_to_visited(self, native):
        try:
            self.cursor.execute('SELECT * FROM words WHERE native = ?', (native,))
            word = self.cursor.fetchone()

            if word:
                self.cursor.execute('SELECT COUNT(*) FROM previously_visited')
                count = self.cursor.fetchone()[0]

                if count >= 9:
                    self.cursor.execute('DELETE FROM previously_visited WHERE ROWID = (SELECT MIN(ROWID) FROM previously_visited)')
                    self.conn.commit()

                self.cursor.execute('INSERT INTO previously_visited (native, translation, progress, status, sentence) VALUES (?, ?, ?, ?, ?)',
                                (word[0], word[1], word[2], word[3], word[4]))
                self.conn.commit()
        except:
            print("Error")

    def get_all_recently(self):
        try:
            self.cursor.execute('SELECT * FROM previously_visited')
            return self.cursor.fetchall()
        except:
            print("Error")