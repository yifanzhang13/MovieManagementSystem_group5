# -*- coding:utf-8 -*-
import pandas as pd
import pymysql
from collections import OrderedDict

from pymysql.converters import escape_string

__version__ = '1.0.0.0'
"""
@brief  :   简介
@details:   详细信息
@author :   mhwen
@date   :   2021-03-29
"""


class MySqlUtils(object):
    """
    mysql工具类

    """
    def __init__(self, con_param):

        self.connection = pymysql.connect(**con_param)

    def query(self, sql, is_dict = False):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        ret = cursor.fetchall()
        if is_dict:
            col_names = [desc[0] for desc in cursor.description]
            result = []
            for row in ret:
                obj_dict = OrderedDict()
                # 把每一行的数据遍历出来放到Dict中
                for index, value in enumerate(row):
                    obj_dict[col_names[index]] = value
                result.append(obj_dict)
            return result
        else:
            return ret

    def query_one(self, sql):
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchone()

    def excute(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()

    def insert(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        return cursor.lastrowid

    def cursor(self):
        return self.connection.cursor()

    def close(self):
        self.connection.close()


class InitData(object):


    def __init__(self):
        con_param = {
            'host': 'localhost',
            'user': 'root',
            'passwd':'root',
            'db': 'comp0022',
            'port': 3306,
            'charset': 'utf8'
        }
        self.con = MySqlUtils(con_param)

    def drop_tables(self):
        table_list = ['library_users', 'library_movies', 'library_tags', 'library_links', 'library_ratings']
        for table_item in table_list:
            sql = "drop table if exists %s" % table_item
            self.con.excute(sql)


    def create_users(self):
        sql = """
            CREATE TABLE if not exists `library_users` (
              `UserID` int(11) NOT NULL,
              PRIMARY KEY (`UserID`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        self.con.excute(sql)

        sql = "SET foreign_key_checks = 0"
        self.con.excute(sql)
        sql = "TRUNCATE table library_users"
        self.con.excute(sql)
        sql = "SET foreign_key_checks = 1"
        self.con.excute(sql)

        user_df = pd.read_csv(r'users.csv', engine='python')
        user_df.columns = ['UserID']
        for index, row in user_df.iterrows():
            sql = "INSERT INTO `library_users` (`UserID`) values (%s)" % row['UserID']
            print(sql)
            self.con.excute(sql)

    def create_movies(self):
        sql = """
            CREATE TABLE if not exists `library_movies` (
              `MovieID` int(11) NOT NULL,
              `MovieTitle` varchar(255) NOT NULL,
              `MovieGenres` varchar(255) NOT NULL,
              PRIMARY KEY (`MovieID`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        self.con.excute(sql)

        sql = "SET foreign_key_checks = 0"
        self.con.excute(sql)
        sql = "TRUNCATE table library_movies"
        self.con.excute(sql)
        sql = "SET foreign_key_checks = 1"
        self.con.excute(sql)

        movies = pd.read_csv(r'movies.csv', sep=",", engine='python')
        movies.columns = ['movieId', 'title', 'genres']
        for index, row in movies.iterrows():
            sql = "INSERT INTO `library_movies` (`MovieID`, `MovieTitle`, `MovieGenres`) values (%s, '%s', '%s')" % (row['movieId'],
                                                                                                                     escape_string(row['title']),
                                                                                                                     escape_string(row['genres']))
            print(sql)
            self.con.excute(sql)

    def create_tags(self):

        sql = """
                   CREATE TABLE if not exists `library_tags` (
                  `id` int(11) NOT NULL AUTO_INCREMENT,
                  `TagContent` varchar(255) NOT NULL,
                  `Timestamp` int(11) NOT NULL,
                  `MovieID_id` int(11) NOT NULL,
                  `UserID_id` int(11) NOT NULL,
                  PRIMARY KEY (`id`),
                  KEY `library_tags_MovieID_id_c6d94589_fk_library_movies_MovieID` (`MovieID_id`),
                  KEY `library_tags_UserID_id_12b1694e_fk_library_users_UserID` (`UserID_id`),
                  CONSTRAINT `library_tags_MovieID_id_c6d94589_fk_library_movies_MovieID` FOREIGN KEY (`MovieID_id`) REFERENCES `library_movies` (`MovieID`),
                  CONSTRAINT `library_tags_UserID_id_12b1694e_fk_library_users_UserID` FOREIGN KEY (`UserID_id`) REFERENCES `library_users` (`UserID`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """
        self.con.excute(sql)

        sql = "SET foreign_key_checks = 0"
        self.con.excute(sql)
        sql = "TRUNCATE table library_tags"
        self.con.excute(sql)
        sql = "SET foreign_key_checks = 1"
        self.con.excute(sql)

        ratings = pd.read_csv(r'tags.csv', sep=",", engine='python')
        ratings.columns = ['userId', 'movieId', 'tag', 'timestamp']
        for index, row in ratings.iterrows():
            try:
                sql = "INSERT INTO `library_tags` (`TagContent`, `Timestamp`, `MovieID_id`, `UserID_id`)" \
                      " values ('%s', %s, %s, %s)" % (escape_string(row['tag']), row['timestamp'], row['movieId'], row['userId'])
                print(sql)
                self.con.excute(sql)
            except Exception as e:
                print(e)


    def create_links(self):

        sql = """
                   CREATE TABLE if not exists `library_links` (
                  `id` int(11) NOT NULL AUTO_INCREMENT,
                  `imdbID` int(11) NOT NULL,
                  `tmdbID` int(11) NOT NULL,
                  `MovieID_id` int(11) NOT NULL,
                  PRIMARY KEY (`id`),
                  KEY `library_links_MovieID_id_b21126f9_fk_library_movies_MovieID` (`MovieID_id`),
                  CONSTRAINT `library_links_MovieID_id_b21126f9_fk_library_movies_MovieID` FOREIGN KEY (`MovieID_id`) REFERENCES `library_movies` (`MovieID`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """
        self.con.excute(sql)

        sql = "SET foreign_key_checks = 0"
        self.con.excute(sql)
        sql = "TRUNCATE table library_links"
        self.con.excute(sql)
        sql = "SET foreign_key_checks = 1"
        self.con.excute(sql)

        ratings = pd.read_csv(r'links.csv', sep=",", engine='python')
        ratings.columns = ['movieId','imdbId','tmdbId']
        for index, row in ratings.iterrows():
            try:
                sql = "INSERT INTO `library_links` (`imdbID`, `tmdbID`, `MovieID_id`)" \
                      " values ('%s', %s, %s)" % (row['imdbId'], row['tmdbId'], row['movieId'])
                print(sql)
                self.con.excute(sql)
            except Exception as e:
                print(e)

    def create_ratings(self):

        sql = """
                   CREATE TABLE `library_ratings` (
                  `id` int(11) NOT NULL AUTO_INCREMENT,
                  `RatingScore` int(11) NOT NULL,
                  `Timestamp` int(11) NOT NULL,
                  `MovieID_id` int(11) NOT NULL,
                  `UserID_id` int(11) NOT NULL,
                  PRIMARY KEY (`id`),
                  KEY `library_ratings_MovieID_id_bf437317_fk_library_movies_MovieID` (`MovieID_id`),
                  KEY `library_ratings_UserID_id_a78829c0_fk_library_users_UserID` (`UserID_id`),
                  CONSTRAINT `library_ratings_MovieID_id_bf437317_fk_library_movies_MovieID` FOREIGN KEY (`MovieID_id`) REFERENCES `library_movies` (`MovieID`),
                  CONSTRAINT `library_ratings_UserID_id_a78829c0_fk_library_users_UserID` FOREIGN KEY (`UserID_id`) REFERENCES `library_users` (`UserID`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """
        self.con.excute(sql)

        sql = "SET foreign_key_checks = 0"
        self.con.excute(sql)
        sql = "TRUNCATE table library_ratings"
        self.con.excute(sql)
        sql = "SET foreign_key_checks = 1"
        self.con.excute(sql)

        ratings = pd.read_csv(r'ratings.csv', sep=",", engine='python')
        ratings.columns = ['userId', 'movieId', 'rating', 'timestamp']
        for index, row in ratings.iterrows():
            try:
                sql = "INSERT INTO `library_ratings` (`RatingScore`, `Timestamp`, `MovieID_id`, `UserID_id`)" \
                      " values (%s, %s, %s, %s)" % (row['rating'], row['timestamp'], row['movieId'], row['userId'])
                print(sql)
                self.con.excute(sql)
            except Exception as e:
                print(e)



if __name__ == '__main__':
    init = InitData()
    #init.drop_tables()
    init.create_users()
    init.create_movies()
    init.create_tags()
    init.create_links()
    init.create_ratings()