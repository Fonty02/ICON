class clausola:
    def __init__(self, head, body=[]):
        self.head = head
        self.body = body

    def __repr__(self):
        rep = self.head
        if self.body:
            rep += " <- "
            for a in self.body:
                rep += a + " & "
            rep = rep[0:len(rep) - 3]
        return rep


class KB:
    def __init__(self, clausole=[], askable=set(), assumable=set(), naf=set()):
        self.clausole = clausole
        self.atomiTesta = {}
        self.askable = askable
        self.assumable = assumable
        self.naf = naf
        for c in clausole:
            self.addClausola(c)

    def addAskable(self, ask):
        self.askable.add(ask)

    def addAssumable(self, ask):
        self.assumable.add(ask)

    def addClausola(self, c):
        self.clausole.append(c)
        if c.head in self.atomiTesta:
            self.atomiTesta[c.head].add(c)
        else:
            self.atomiTesta[c.head] = set()
            self.atomiTesta[c.head].add(c)

    def addNAF(self, c):
        self.naf.add(c)

    def __repr__(self):
        rep = ""
        for c in self.clausole:
            rep += str(c) + "\n"
        return rep

    def clausolePerTesta(self, a):
        if a in self.atomiTesta:
            return self.atomiTesta[a]
        else:
            return set()

    def _fixedPoint_(self):
        fp = set()
        added = True
        while added:
            added = False
            for c in self.clausole:
                if c.head not in fp and all(b in fp for b in c.body):
                    fp.add(c.head)
                    added = True
        return fp

    def BottomUp(self, proposition):
        return "True" if all(b in self._fixedPoint_() for b in proposition) else "False"

    def TopDown(self, preposition):
        if preposition:
            selezionata = preposition[0]
            return any(self.TopDown(cl.body + preposition[1:]) for cl in self.clausolePerTesta(selezionata))
        else:
            return True

    def prove_atom(self, atom, indent=""):
        if atom in self.askable:
            if input("Is " + atom + " true? ") == "Y":
                return (atom, "answered")
            else:
                return "fail"
        else:
            for cl in self.clausolePerTesta(atom):
                pr_body = self.prove_body(cl.body, indent)
                if pr_body != "fail":
                    return (atom, pr_body)
            return "fail"

    def prove_body(self, ans_body, indent=""):
        proofs = []
        for atom in ans_body:
            proof_at = self.prove_atom(atom, indent + " ")
            if proof_at == "fail":
                return "fail"  # fail if any proof fails
            else:
                proofs.append(proof_at)
        return proofs

    def prove_all_assumable(self, ans_body, assumed=None):
        if assumed is None:
            assumed = set()
        if ans_body:
            selected = ans_body[0]
            if selected in self.askable:
                if (input("Is " + selected + " true? ")=="Y"):
                    return self.prove_all_assumable(ans_body[1:], assumed)
                else:
                    return []  # no answers
            elif selected in self.assumable:
                return self.prove_all_assumable(ans_body[1:], assumed | {selected})
            else:
                return [ass
                        for cl in self.clausolePerTesta(selected)
                        for ass in self.prove_all_assumable(cl.body + ans_body[1:], assumed)]
        else:
            return assumed

    def conflicts(self):
        return self.minsets(self.prove_all_assumable(['false']))

    def minsets(self, ls):
        ans = []
        for c in ls:
            if not any(c1 < c for c1 in ls) and not any(c1 <= c for c1 in ans):
                ans.append(c)
        return ans

    def diagnoses(self, cons):
        if cons == []:
            return [set()]
        else:
            return self.minsets([({e} | d)
                                 for e in cons[0]
                                 for d in self.diagnoses(cons[1:])])

    def prove_naf(self, ans_body, indent=""):
        print(2, indent, 'yes <-', ' & '.join(str(e) for e in ans_body))
        if ans_body:
                selected = ans_body[0]  # select first atom from ans_body
                if selected in self.naf:
                    print(2, indent, f"proving {selected.atom()}")
                    if self.prove_naf([selected.atom()], indent):
                        print(2, indent, f"{selected.atom()} succeeded so Not({selected.atom()})fails")
                        return False
                    else:
                        print(2, indent, f"{selected.atom()} fails soNot({selected.atom()})succeeds")
                        return self.prove_naf(ans_body[1:], indent + " ")
                if selected in self.askables:
                    return (input("Is " + selected + " true? ")=="Y") and self.prove_naf(ans_body[1:], indent + " ")
                else:
                    return any(self.prove_naf(cl.body + ans_body[1:], indent + " ")
                                   for cl in self.clausolePerTesta(selected))
        else:
            return True
