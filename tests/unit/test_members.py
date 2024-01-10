from unittest import TestCase
from family_tree.member import Member,Gender
from unittest.mock import patch,Mock


def create_fake_member(id=None,name=None,gender=None,
    spouse=None,father=None,mother=None,children=None):
    member = Mock()
    member.id = id
    member.name = name
    member.mother = mother
    member.father = father
    member.spouse = spouse
    member.children = children
    return member

class TestMember(TestCase):

    def setUp(self):
        self.member= Member(1,"Yusuf","Male")
   
    def test_initialization(self):
        # check instance
        self.assertEqual(isinstance(self.member,Member),True)
        # check properties
        self.assertEqual(self.member.id,1)
        self.assertEqual(self.member.name,"Yusuf")
        self.assertEqual(self.member.gender,Gender.male)
        self.assertEqual(self.member.mother,None)
        self.assertEqual(self.member.father,None)
        self.assertEqual(self.member.spouse,None)
        self.assertEqual(self.member.children,[])

        # edge case for gender
        self.assertRaises(ValueError,Member,2,"SomeOtherPerson","Queer")

    def test_set_mother(self):
        mother_demo_a = "mother_demo_a"
        mother_demo_b = Member(2,"MotherDemoB","Male")
        mother_demo_c = Member(3,"Mom","Female")
        
        # error case
        self.assertRaises(ValueError,self.member.set_mother,mother_demo_a)
        self.assertRaises(ValueError,self.member.set_mother,mother_demo_b)
        
        # success case
        self.member.set_mother(mother_demo_c)
        self.assertEqual(self.member.mother.name,"Mom")
        self.assertEqual(self.member.mother.gender,Gender.female)
    
    def test_set_father(self):
        father_demo_a = "father_demo_a"
        father_demo_b = Member(4,"FatherDemoB","Female")
        father_demo_c = Member(3,"Boya","Male")
        
        # error case
        self.assertRaises(ValueError,self.member.set_father,father_demo_a)
        self.assertRaises(ValueError,self.member.set_father,father_demo_b)
        
        # success case
        self.member.set_father(father_demo_c)
        self.assertEqual(self.member.father.name,"Boya")
        self.assertEqual(self.member.father.gender,Gender.male)

    def test_set_spouse(self):
        spouse_demo_a = "spouse_demo_a"
        spouse_demo_b = Member(4,"SpouseDemoB","Male")
        spouse_demo_c = Member(5,"Wife","Female")
        
        # error case
        self.assertRaises(ValueError,self.member.set_spouse,spouse_demo_a)
        self.assertRaises(ValueError,self.member.set_spouse,spouse_demo_b)
        
        # success case
        self.member.set_spouse(spouse_demo_c)
        self.assertEqual(self.member.spouse.name,"Wife")
        self.assertEqual(self.member.spouse.gender,Gender.female)

    def test_add_child(self):
        child_demo_a = "child_demo_a"
        child_demo_b = Member(4,"Daughter","Female")
        
        # error case
        self.assertRaises(ValueError,self.member.add_child,child_demo_a)
        
        # success case
        self.member.add_child(child_demo_b)
        self.assertEqual(self.member.children[0].name,"Daughter")
        self.assertEqual(self.member.children[0].gender,Gender.female)

    def test_get_paternal_grandmother(self):
        member = Member(9,"NewMember","Male")
        father = Member(10,"NewMember_father","Male")
        grandmother = Member(11,"Newmember_grandmother","Female")
        
        # error case
        self.assertEqual(member.get_paternal_grandmother(),None)

        member.father = father
        self.assertEqual(member.get_paternal_grandmother(),None)

        member.father.mother = grandmother
        self.assertEqual(member.get_paternal_grandmother(),grandmother)

    def test_get_maternal_grandmother(self):
        member = Member(9,"NewMember","Male")
        mother = Member(10,"NewMember_mother","Female")
        grandmother = Member(11,"Newmember_grandmother","Female")
        
        # error case
        self.assertEqual(member.get_maternal_grandmother(),None)

        member.mother = mother
        self.assertEqual(member.get_maternal_grandmother(),None)

        member.mother.mother = grandmother
        self.assertEqual(member.get_maternal_grandmother(),grandmother)

    def test_get_spouse_mother(self):
        member = Member(9,"Newmember","Male")
        spouse = Member(10,"Newmember_spouse","Female")
        spouse_mother = Member(11,"Newmember_spousemother","Female")

        # error case
        self.assertEqual(member.get_spouse_mother(),None)

        member.spouse = spouse
        self.assertEqual(member.get_spouse_mother(),None)
        
        member.spouse.mother = spouse_mother
        self.assertEqual(member.get_spouse_mother(),spouse_mother)

    @patch('family_tree.member.Member.get_paternal_grandmother',side_effect=[
        None,
        create_fake_member(),
        create_fake_member(children=[Member(3,"Boya","Male")]),
        create_fake_member(children=[Member(3,"Boya","Male"),
                                     Member(4,"Uncle","Male")
                                     ]),
        create_fake_member(children=[Member(3,"Boya","Male"),
                                     Member(4,"Uncle","Male"),
                                     Member(5,"Aunt","Female")
                                     ])
        

           ])
    def test_get_paternal_aunt(self,mock_get_paternal_grandmother):
        # check if get_paternal_grandmother has been replaced by a mock
        self.assertEqual(isinstance(self.member.get_paternal_grandmother,Mock),True)
        
        # check for None values
        self.assertEqual(self.member.get_paternal_aunt(),[])
        self.assertEqual(self.member.get_paternal_aunt(),[])
        self.assertEqual(self.member.get_paternal_aunt(),[])
        self.assertEqual(self.member.get_paternal_aunt(),[])

        # self.assertEqual(len(self.member.get_paternal_aunt()),1)
        self.assertEqual(self.member.get_paternal_aunt()[0].name,"Aunt")
        # self.assertEqual(self.member.get_paternal_aunt()[0].gender,Gender.female)
        # to check that the mock_get_paternal_grandmother was called instead of self.member.get_paternal_grandmother
        mock_get_paternal_grandmother.assert_called_with()

