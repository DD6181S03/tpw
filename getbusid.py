#coding: utf-8
import requests
import sqlite3
import time 

conn = sqlite3.connect('somedata.db')
cursor = conn.cursor()

tlist = [5, 6, 7, 8, 9, 10, 11, 12, 17, 18, 23, 24, 27, 28, 31, 32, 37, 38, 39, 40, 41, 42, 47, 48, 53, 54, 55, 56, 59, 60, 61, 62, 64, 77, 78, 80, 81, 82, 85, 86, 87, 88, 93, 94, 95, 96, 97, 98, 99, 100, 105, 106, 107, 108, 113, 114, 117, 118, 119, 122, 123, 127, 128, 131, 132, 133, 134, 137, 138, 141, 142, 145, 146, 147, 148, 151, 152, 153, 154, 157, 163, 164, 165, 166, 169, 170, 173, 174, 179, 180, 183, 185, 186, 187, 188, 191, 193, 195, 196, 197, 198, 199, 200, 201, 202, 208, 209, 217, 218, 219, 220, 221, 222, 223, 224, 227, 233, 234, 235, 236, 239, 240, 241, 242, 247, 248, 255, 256, 257, 258, 261, 262, 269, 270, 273, 274, 285, 286, 294, 298, 306, 320, 330, 333, 363, 364, 367, 368, 371, 372, 373, 374, 375, 376, 377, 378, 381, 382, 397, 398, 417, 420, 427, 428, 429, 430, 431, 432, 440, 441, 442, 443, 444, 445, 446, 447, 496, 497, 514, 517, 518, 519, 520, 521, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 535, 536, 537, 540, 541, 550, 551, 552, 553, 556, 557, 558, 559, 566, 567, 568, 569, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 585, 586, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 634, 635, 636, 638, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 662, 663, 666, 667, 668, 669, 679, 680, 681, 682, 683, 684, 685, 688, 690, 692, 693, 696, 697, 712, 713, 715, 716, 719, 720, 723, 724, 725, 730, 731, 732, 733, 734, 738, 739, 744, 755, 756, 759, 762, 763, 764, 773, 774, 775, 776, 783, 784, 785, 786, 789, 791, 799, 800, 812, 813, 814, 816, 824, 825, 836, 837, 838, 839, 853, 868, 871, 872, 881, 882, 899, 909, 912, 913, 914, 917, 918, 920, 921, 922, 923, 928, 929, 935, 944, 945, 946, 947, 948, 949, 950, 951, 953, 954, 955, 956, 957, 958, 959, 960, 961, 963, 971, 972]
headers = {'version': 'android-insigma.waybook.jinan-2363', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0'}

llist = []
while True:
    for lineid in tlist:
        url = 'http://iwaybook.369cx.cn/server-ue2/rest/buses/busline/370100/' + str(lineid)
        r = requests.get(url,headers=headers).json()['result']
        if r:
            for item in r:
                busid = item['busId']
                buslineid = item['buslineId']
                cursor.execute('REPLACE INTO busidtoline (busid,line) VALUES (?,?)',(busid,buslineid))
                conn.commit()
    
    time.sleep(600)

cursor.close()
conn.close()