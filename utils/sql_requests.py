CREATE_USERS_TABLE = '''
                        CREATE TABLE users
                        (
                            user_id SERIAL PRIMARY KEY,
                            first_name VARCHAR(100) NOT NULL,
                            last_name VARCHAR(100) NOT NULL,
                            email VARCHAR(100) UNIQUE NOT NULL
                        );
                    '''

CREATE_PHONES_TABLE = '''
                        CREATE TABLE phones
                        (
                            phone_id SERIAL PRIMARY KEY,
                            phone VARCHAR(20) UNIQUE NOT NULL,
                            user_id INT REFERENCES users(user_id)
                        );
                    '''

INSERT_USERS_TABLE = '''
                        INSERT INTO users (first_name, last_name, email)
                        VALUES(%s, %s, %s) RETURNING user_id;
                    '''

INSERT_PHONES_TABLE = '''
                        INSERT INTO phones (phone, user_id)
                        VALUES(%s, %s);
                    '''

SELECT_USER_BY_FIRST_NAME = '''
                        SELECT user_id, first_name, last_name, email, phone FROM users
                        LEFT JOIN phones USING (user_id)
                        WHERE first_name = %s;
                    '''

SELECT_USER_BY_LAST_NAME = '''
                            SELECT user_id, first_name, last_name, email, phone FROM users
                            LEFT JOIN phones USING (user_id)
                            WHERE last_name = %s;
                        '''

SELECT_USER_BY_EMAIL = '''
                            SELECT user_id, first_name, last_name, email, phone FROM users
                            LEFT JOIN phones USING (user_id)
                            WHERE email = %s;
                        '''

SELECT_USER_BY_PHONE = '''
                            SELECT user_id, first_name, last_name, email, phone FROM phones
                            JOIN users USING (user_id)
                            WHERE phone = %s;
                        '''

UPDATE_FIRST_NAME_USERS = '''
                            UPDATE users
                            SET first_name = %s
                            WHERE user_id = %s;
                        '''

UPDATE_LAST_NAME_USERS = '''
                            UPDATE users
                            SET last_name = %s
                            WHERE user_id = %s;
                        '''

UPDATE_EMAIL_USERS = '''
                            UPDATE users
                            SET email = %s
                            WHERE user_id = %s;
                    '''

DROP_USERS_TABLE = 'DROP TABLE IF EXISTS users CASCADE;'

DROP_PHONES_TABLE = 'DROP TABLE IF EXISTS phones CASCADE;'

DELETE_PHONE_PHONES = '''
                        DELETE FROM phones
                        WHERE phone = %s;
                    '''
DELETE_USER_USERS = '''
                        DELETE FROM phones
                        WHERE user_id = %(id)s;
                        DELETE FROM users
                        WHERE user_id = %(id)s;
                    '''
