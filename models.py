# coding=utf-8
import conn
import getpass
from func import match_site, dna_to_rna, rna_to_pro


class User(object):
    def __init__(self, uid, name):
        self.id = uid
        self.name = name

    def choice_management(self):
        while 1:
            print '\nSelect management to continue: '
            print '1. Enzyme Management'
            print '2. DNA Management'
            print 'Input \'q\' to exit.'

            choice = raw_input('Enter: ')
            if choice == '1':
                self.enzyme_management()
            elif choice == '2':
                self.dna_management()
            else:
                raise SystemExit

    def _list_enzyme(self):
        data = conn.c.execute('SELECT id, name, site FROM enzyme WHERE uid=?', (self.id, ))
        enzymes = data.fetchall()
        print
        print 'id'.rjust(24), 'name'.rjust(40), 'site'.rjust(24)
        print '-' * 91
        for enzyme in enzymes:
            print str(enzyme[0]).rjust(24), str(enzyme[1]).rjust(40), str(enzyme[2]).rjust(24)

    def _list_dna(self):
        data = conn.c.execute('SELECT id, sequence FROM gene WHERE uid=?', (self.id, ))
        dnas = data.fetchall()
        print
        print 'id'.rjust(10), 'sequence'.rjust(80)
        print '-' * 91
        for dna in dnas:
            print str(dna[0]).rjust(10), (dna[1][:60] + '...').rjust(80)

    def enzyme_management(self):
        print
        print '1. Add enzyme'
        print '2. Modify enzyme'
        print '3. Delete enzyme'
        print '4. List enzymes'
        print 'Input \'q\' to back.'

        choice = raw_input('Please choose the operation: ')

        if choice == '1':
            e_name = raw_input('Enter the enzyme name: ')
            e_site = raw_input('Enter the enzyme site: ')
            if len(e_site) != 2 or not self.check_dna(e_site):
                print 'Illegal site'
                return self.enzyme_management()

            conn.c.execute('INSERT INTO enzyme (name, site, uid) VALUES (?, ?, ?)', (e_name, e_site, self.id))
            conn.conn.commit()
            print 'Record created successfully'

        elif choice == '2':
            self._list_enzyme()
            eid = raw_input('Enter the enzyme id you want to modify: ')
            n_e = raw_input('Enter the enzyme name: ')
            s_e = raw_input('Enter the new enzyme site: ')
            if len(s_e) != 2 or not self.check_dna(s_e):
                print 'Illegal site'
                return

            conn.c.execute('UPDATE enzyme SET name=?, site=? WHERE id=? and uid=?', (n_e, s_e, eid, self.id))
            conn.conn.commit()
            print 'Record changes successfully'

        elif choice == '3':
            self._list_enzyme()
            enzyme_id = raw_input('Enter the enzyme id you want to delete: ')
            conn.c.execute('DELETE from enzyme where id=? and uid=?', (enzyme_id, self.id))
            conn.conn.commit()

        elif choice == '4':
            self._list_enzyme()
        elif choice == 'q':
            return
        return self.enzyme_management()

    def _list_site(self, gid):
        print
        data = conn.c.execute('SELECT eg.eid, e.site, e.name FROM enzyme_gene eg '
                              'LEFT JOIN enzyme e ON e.id = eg.eid WHERE gid=? GROUP BY eid', (gid, ))
        sites = data.fetchall()
        print 'eid'.ljust(10), 'name'.ljust(20), 'site'.ljust(10)
        print '-' * 91
        for i in sites:
            eid, site, name = i
            print str(eid).ljust(10), str(name).ljust(20), str(site).ljust(10)

        dna = conn.c.execute('SELECT sequence FROM gene WHERE id=?', (gid, ))
        sequence = dna.fetchone()
        if not sequence:
            return
        else:
            sequence = sequence[0]

        for site in sites:
            _, site, _ = site
            print '-' * 25
            positions = match_site(site, sequence)
            count = 0
            lines = len(sequence) / 20
            if len(sequence) % 20:
                lines += 1

            for i in range(lines):
                string_arrow = ''
                string_count = ''
                string_sequence = sequence[i*20:i*20+20]
                for j in range(0, len(string_sequence)):
                    if j == 10:
                        string_count += ' '
                        string_arrow += ' '
                    if count < len(positions) and int(positions[count]) == (j + i * 20):
                        string_count += str(count + 1)
                        string_arrow += '|'
                        count += 1
                    else:
                        string_count += ' '
                        string_arrow += ' '

                print string_sequence[:10], string_sequence[10:]
                print string_arrow
                print string_count

    def check_dna(self, sequence):
        for i in set(sequence):
            if i not in ('A', 'T', 'C', 'G'):
                return False
        return True

    def dna_management(self):
        print
        print '1. Add DNA sequence'
        print '2. Modify DNA sequence'
        print '3. Delete DNA sequence'
        print '4. Add restriction enzyme cutting sites'
        print '5. List DNA sequence list'
        print '6. List restriction enzyme cutting sites'
        print '7. Translate DNA to protein'
        print '8. Visual output bp'
        print 'Input \'q\' to back.'

        choice = raw_input('Please choose the operation: ')

        if choice == '1':
            the_gene = raw_input('Enter the DNA sequence: ')
            the_gene = the_gene.replace('\n', '')
            if self.check_dna(the_gene):
                conn.c.execute('INSERT INTO gene (sequence, uid) VALUES (?, ?)', (the_gene, self.id))
                conn.conn.commit()
                print 'Record created successfully'
            else:
                print 'Invalid DNA sequence'

        elif choice == '2':
            self._list_dna()
            d_id = raw_input('Enter the DNA id you want to modify: ')
            d_seq = raw_input('Enter the new DNA sequence: ')
            d_seq = d_seq.replace('\n', '')
            if self.check_dna(d_seq):
                conn.c.execute('UPDATE gene SET sequence=? WHERE id=? and uid=?', (d_seq, d_id, self.id))
                conn.conn.commit()
                print 'Record changes successfully'
            else:
                print 'Invalid DNA sequence'

        elif choice == '3':
            self._list_dna()
            d_id = raw_input('Enter the DNA sequence id you want to delete: ')
            conn.c.execute('DELETE from gene where id=? and uid=?', (d_id, self.id))
            conn.conn.commit()

        elif choice == '4':
            print 'DNA list:'
            self._list_dna()
            dna_id = raw_input('Please choose DNA sequence id: ')
            data = conn.c.execute('SELECT id, sequence FROM gene WHERE id=? and uid=?', (dna_id, self.id))
            dna = data.fetchone()
            if not dna:
                print 'DNA dose not exist, please add it first.'
                return self.dna_management()

            print 'Enzyme list:'
            self._list_enzyme()
            enzyme_id = raw_input('Please choose enzyme id: ')
            data = conn.c.execute('SELECT id, name, site FROM enzyme WHERE id=? and uid=?', (enzyme_id, self.id))
            enzyme = data.fetchone()
            if not enzyme:
                print 'Enzyme dose not exist, please add it first.'
                return self.dna_management()

            eid, name, site = enzyme
            gid, sequence = dna

            conn.c.execute('INSERT INTO enzyme_gene (eid, gid) VALUES (?, ?)', (eid, gid))
            conn.conn.commit()
            positions = match_site(site, sequence)
            print '-' * 91
            print str(eid).ljust(10), str(name).ljust(20), str(site).ljust(10), \
                str(','.join(map(str, positions))).rjust(48)

        elif choice == '5':
            self._list_dna()
        elif choice == '6':
            print 'DNA list:'
            self._list_dna()
            gid = raw_input('Please choose DNA sequence id: ')
            self._list_site(gid)
        elif choice == '7':
            self._list_dna()
            gid = raw_input('Enter DNA id: ')
            dna_sequence = conn.c.execute('SELECT sequence FROM gene WHERE id=?', (gid, )).fetchone()
            if dna_sequence:
                dna_sequence = dna_sequence[0]
                print 'DNA sequence:', dna_sequence
                rna_sequence = dna_to_rna(dna_sequence)
                print 'mRAN sequence:', rna_sequence
                print 'Protein sequence from the first bp:', rna_to_pro(rna_sequence, 0)
                print 'Protein sequence from the second bp:', rna_to_pro(rna_sequence, 1)
                print 'Protein sequence from the third bp:', rna_to_pro(rna_sequence, 2)
                print 'Protein sequence from the last bp:', rna_to_pro(rna_sequence, -1)
                print 'Protein sequence from the second last bp:', rna_to_pro(rna_sequence, -2)

        elif choice == '8':
            self._list_dna()
            gid = raw_input('Enter DNA id: ')
            dna_sequence = conn.c.execute('SELECT sequence FROM gene WHERE id=?', (gid, )).fetchone()

            width = 200
            point_map = {
                0: '#',
                1: '+',
                2: '*',
                3: '-',
            }
            if dna_sequence:
                print '-' * (width / 2 + 6)
                dna_sequence = dna_sequence[0]
                result = []
                for i in range(0, width, 2):
                    dna_sequence_temp = dna_sequence[i:i+1000]
                    result.append(map(dna_sequence_temp.count, ('A', 'C', 'T', 'G')))
                result = map(list, zip(*result))
                union_list = []
                for i in result:
                    union_list.extend(i)
                union_list.sort()

                ordered_set = []
                for i in union_list:
                    if i not in ordered_set:
                        ordered_set.append(i)
                ordered_set = ordered_set[::-1]

                for value in ordered_set:
                    points = []
                    for index, bp in enumerate(result):
                        _ = match_site(value, bp)
                        _ = [{i: index} for i in _]
                        points.extend(_)
                    points.sort()
                    line = ''

                    for i in range(0, width / 2):
                        row = map(lambda x: x.keys()[0], points)
                        if i in set(row):
                            line += point_map[points[row.index(i)][i]]
                        else:
                            line += ' '
                    print str(value).ljust(5), line
                print '-' * (width / 2 + 6)
                print 'A: #, C: +, T: *, G: -'

        elif choice == 'q':
            return
        return self.dna_management()


class Admin(User):
    def choice_management(self):
        while 1:
            print '\nSelect management to continue: '
            print '1. User Management'
            print '2. Enzyme Management'
            print '3. DNA Management'
            print 'Input \'q\' to exit.'

            choice = raw_input('Enter: ')
            if choice == '1':
                self.user_management()
            elif choice == '2':
                self.enzyme_management()
            elif choice == '3':
                self.dna_management()
            else:
                raise SystemExit

    def user_management(self):
        while 1:
            print '\nUser Management'
            print '1. Add user'
            print '2. Delete user'
            print '3. Modify user'
            print '4. List users'
            print 'Input \'q\' to back.'

            choice = raw_input('Enter: ')
            if choice == '1':
                self._add_user()
            elif choice == '2':
                self._delete_user()
            elif choice == '3':
                self._update_user()
            elif choice == '4':
                self._list_users()
            else:
                break

    def _list_users(self):
        data = conn.c.execute('SELECT id, username, is_admin FROM user')
        print
        print 'id'.rjust(10), 'name'.rjust(20), 'is_admin'.rjust(10)
        print '-' * 43
        users = data.fetchall()
        for user in users:
            print str(user[0]).rjust(10), str(user[1]).rjust(20), str(user[2]).rjust(10)
        print '-' * 43

    def _add_user(self):
        new_name = raw_input('Enter new username: ')
        data = conn.c.execute('SELECT * FROM user WHERE username=?', (new_name, ))
        if data.fetchall():
            print 'Username \'', new_name, '\' already existed.\n'
            return self._add_user()
        new_password = getpass.getpass('Enter password: ')
        is_admin = raw_input('Admin enter 1, ordinary user enter 0: ')
        conn.c.execute('INSERT INTO user(username, password, is_admin) VALUES (?,?,?)',
                       (new_name, new_password, is_admin))
        conn.conn.commit()
        print '\nRecord created successfully\n'

    def _delete_user(self):
        self._list_users()
        uid = raw_input('\nEnter the id which you will delete: ')
        conn.c.execute('DELETE from user where id=?;', (uid, ))
        conn.conn.commit()
        print '\nRecord deleted successfully\n'

    def _update_user(self):
        self._list_users()
        uid = raw_input('Enter the id which you will update: ')
        print
        u_name = raw_input('Enter the username you changed: ')
        u_password = raw_input('Enter the new password: ')
        u_admin = raw_input('Admin enter 1,ordinary user enter 0: ')
        conn.c.execute('UPDATE user SET username=?, password=?, is_admin=? WHERE id=?',
                       (u_name, u_password, u_admin, uid))
        conn.conn.commit()
        print '\nRecord updated successfully\n'
