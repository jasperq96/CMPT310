import copy as c
"""
-----------------------User Commands-----------------------
"tell" command tells KB what is true.

"infer_all" command combines the knowledge and concludes, adds conclusion to atoms

"load file_name.txt" command loads into memory the KB stored in the file
Thoughts
- set head as dictionary name, atoms are the entries in the dictionary. 
- include a top entry that concludes if the lower atoms are all true

"end" command ends the program


-----------------PSEUDOCODE for infer_all(KB)--------------
Algorithm infer_all(KB)
  Input : KB, containing rules and atoms
  Output: set of all atoms that are logical consequences
          of KB

  set C to {}   // C contains the inferred atoms

  loop until no more rules from KB can be selected:
     select a rule "h <-- a_1 & a_2 & ... & a_n" from KB
            where all a_i are in C or KB (for 1 <= i <= n)
                  and h is not in C or KB
     add atom h to C

  return C
"""

def infer_all(knowledge_base, atoms_known):
	inferred = []
	prev_infer = -1

	while prev_infer < len(inferred):
		prev_infer = len(inferred)
		for key in knowledge_base:
			# if type(knowledge_base[key]) == str:
			# 	if knowledge_base[key] == "in":
			# 		atoms_known.append(key)
			if key not in inferred:
				#for x in knowledge_base[key]:
					# if knowledge_base[key][x] == "in":
					# 	atoms_known.append(x)
				check = knowledge_base[key].values()
				if "out" not in check and key not in inferred and key not in atoms_known:
					inferred.append(key)
					tell([key], False, atoms_known)
				

	print("Newly Inferred Atoms:")
	print("  ", end='')
	if len(inferred) > 0:
		for x in range(len(inferred)):
			if x < len(inferred)-1:
				print(f'{inferred[x]}, ', end='')
			else:
				print(f'{inferred[x]}')
	else:
		print("<None>")

	print("\nAtoms already known to be true:")
	print("  ", end='')
	for x in range(len(atoms_known)):
		if x < len(atoms_known)-1:
			print(f'{atoms_known[x]}, ', end='')
		else:
			print(f'{atoms_known[x]}')

	for atom in inferred:
		atoms_known.append(atom)

	print("\n")

def tell(input_atoms, not_infer, atom_list):
	if KB_up:
		valid = True
		for atom in input_atoms:
			if not is_atom(atom):
				if not_infer:
					print(f'Error: "{atom}" is not a valid atom\n')
				valid = False
				break
		if valid:
			for atom in input_atoms:
				not_in_KB = True
				recur = False
				for key in KB:
					if key == atom:
						if not_infer:
							print(f'atom "{atom}" is a header, not an atom\n')
						not_in_KB = False
						break
					else:
						for checklist in KB[key]:
							if checklist == atom:
								if KB[key][checklist] != "in":
									KB[key][checklist] = "in"
									if not_infer and not recur:
										print(f'"{atom}" added to KB')
										#print(recur)
										atom_list.append(atom)
										recur = True
								elif not_infer:
									print(f'atom "{atom}" already known to be true\n')
								not_in_KB = False
								break
					# if not not_in_KB:
					# 	break
				if not_in_KB: #add to KB if atom does not exist
					# KB[atom] = "in"
					print(f'"{atom}" is not a valid atom\n')
	else:
		print("There is no Knowledge Base\n")

# returns True if, and only if, string s is a valid variable name
def is_atom(s):
    if not isinstance(s, str):
        return False
    if s == "":
        return False
    return is_letter(s[0]) and all(is_letter(c) or c.isdigit() for c in s[1:])

def is_letter(s):
    return len(s) == 1 and s.lower() in "_abcdefghijklmnopqrstuvwxyz"

KB_up = False
one_tell = False


while True:
	user_input = input("kb> ").split()
	if user_input[0] == "end":
		print("Closing Knowledge Base")
		break
	elif user_input[0] == "tell":
		if len(user_input) == 1:
			print("Error: tell needs at least one atom\n")
		else:
			one_tell = True
			tell(user_input[1:], True, already_known)
			#print("known :", already_known)
	elif user_input[0] == "infer_all":
		if KB_up and one_tell:
			infer_all(KB, already_known)
		else:
			print("Need Knowledge base or 1 'tell' command first\n")
	elif user_input[0] == "load":
		
		if len(user_input) == 1:
			print("Error: load needs a file name\n")
		else:
			KB = {}
			rules_list = []
			already_known= []
			KB_incorrect = False
			f = open(user_input[1], 'r')
			content = f.readlines()
			#print(f'Content : {content}')
			rules = 0
			for lines in content[::2]:
				rules += 1
				rules_list.append(lines)
				rule = lines.split()
				if rule[1] == "<--" and is_atom(rule[0]):
					#print(rule)
					head = rule[0]
					KB[head] = {}
					for x in range(2,len(rule),2): #len() starts at 1 not 0
						atom = rule[x]
						#print("atom: ", atom)
						if x+1 < len(rule): 
							sign = rule[x+1]
							if sign != "&":
								print(f'Error: {user_input[1]} is not a valid knowledge base\n')
								KB_incorrect = True
								break
							else:
								KB[head][atom] = "out"
						else:
							KB[head][atom] = "out"
				else:
					print(f'Error: {user_input[1]} is not a valid knowledge base\n')
					break
				if KB_incorrect:
					break
			if not KB_incorrect:
				KB_up = True
				for x in rules_list:
					print(x, end='')
				print(f'\n\n{rules} new rule(s) added\n')
				#print("The KB is now: ", KB)
				backup_KB = c.deepcopy(KB)
			f.close()
	elif user_input[0] == "clear_atoms":
		if KB_up:
			KB = c.deepcopy(backup_KB)
			already_known.clear()
			#print(f'Cleared KB {KB}')
			print("Reset Atoms")
		else:
			print("There is currently no Knowledge Base\n")
	elif user_input[0] == "print":
		if KB_up:
			for key in KB:
				print(key, ":", KB[key])
		else:
			print("There is currently no Knowledge Base\n")
	else:
		print(f'Error: unknown command {user_input[0]}\n')