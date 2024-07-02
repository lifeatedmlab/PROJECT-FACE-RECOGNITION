from database import mydb, mycursor

def get_next_person_number():
    mycursor.execute("select ifnull(max(prs_nbr) + 1, 101) from prs_mstr")
    row = mycursor.fetchone()
    return row[0]

def add_person(prsnbr, prsname, prsskill):
    mycursor.execute("""INSERT INTO `prs_mstr` (`prs_nbr`, `prs_name`, `prs_skill`) VALUES
                    ('{}', '{}', '{}')""".format(prsnbr, prsname, prsskill))
    mydb.commit()
