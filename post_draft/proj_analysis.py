
import sqlite3 as lite
import matplotlib.pyplot as plt
import numpy as np

def import_data_by_offset(path):
    data = {}

    con = lite.connect(path)
    with con:
        cur = con.cursor()
        for i in range(20):
            if i % 2 != 0:
                data[i] = {}
                for j in range(30):
                    data[i][j] = []
                    for entry in cur.execute(
                        "SELECT * FROM ProjResults WHERE Offset = %d AND Cushion = %d" 
                        % (i, j)):
                        data[i][j].append(entry)

    return data

def find_percent_still_avail(data, by):
    percentages = {}
    if by == "offset":
        for i in range(20):
            if i % 2 != 0:
                percentages[i] = {}
                for j in range(30):
                    percentages[i][j] = []
                    total = 0
                    num   = 0.0
                    for entry in data[i][j]:
                        if entry[3]:
                            total += 1
                        num += 1
                    #print "Total:", total
                    #print "Num:", num
                    #print "t / n:", total / num
                    percentages[i][j] = total / num
    return percentages

def plot_results(offset, data):

    x = range(30)
    y = []
    for i in range(30):
        y.append(data[i])

    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)

    xp= np.linspace(0, 30, 100)

    plt.scatter(x, y)
    plt.plot(xp, p(xp), "-")

    plt.title("Probability of Remaining for %d Picks" % offset)
    plt.ylabel("Probability")
    plt.xlabel("Distance From Best Ranked Available")
    plt.show()

def export_csv(data):
    w = open('output.csv', 'w')
    string = ""
    for i in range(30):
        string += ", " + str(i)
    w.write(string + "\n")
    for i in range(1, 18, 2):
        string = str(i)
        for j in range(30):
            string += ", " + str(data[i][j])
        w.write(string + "\n")
    w.close()

def export_csv_alt(data):
    w = open('output.csv', 'w')
    string = ""
    for i in range(1, 18, 2):
        string += ", " + str(i)
    w.write(string + "\n")
    for i in range(30):
        string = str(i)
        for j in range(1, 18, 2):
            string += ", " + str(data[j][i])
        w.write(string + "\n")
    w.close()

def row_to_string(row):
    row_s = []
    for item in row:
        row_s.append(str(item))
    return row_s
            

if __name__ == '__main__':
    path = "../data/projection_data.db"
    data = import_data_by_offset(path)
    percentages = find_percent_still_avail(data, "offset")
    plot_results(7, percentages[7])
    export_csv_alt(percentages)
 
        
