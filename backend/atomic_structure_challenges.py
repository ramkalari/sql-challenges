ATOMIC_STRUCTURE_CHALLENGES = [
    {
        "id": 101,
        "name": "What is an Atom?",
        "level": "Basic",
        "question": "An atom is the smallest unit of matter. Which of the following best describes the structure of an atom?",
        "type": "multiple_choice",
        "options": [
            "A solid ball with no internal structure",
            "A nucleus (protons and neutrons) surrounded by electrons in shells",
            "Only protons and electrons mixed together", 
            "A hollow sphere with particles floating inside"
        ],
        "correct_answer": 1,
        "explanation": "An atom consists of a nucleus containing protons and neutrons, with electrons revolving around it in fixed paths called shells (K, L, M, N).",
        "expected_output": ["B"]
    },
    {
        "id": 102,
        "name": "Electron Shells",
        "level": "Basic", 
        "question": "Electrons revolve around the nucleus in fixed paths. What are these paths called?",
        "type": "multiple_choice",
        "options": [
            "Orbits or shells",
            "Rings", 
            "Circles",
            "Tracks"
        ],
        "correct_answer": 0,
        "explanation": "Electrons move in fixed circular paths around the nucleus called shells or orbits, labeled as K, L, M, N (from innermost to outermost).",
        "expected_output": ["A"]
    },
    {
        "id": 103,
        "name": "Neutral Atoms",
        "level": "Basic",
        "question": "Why is an atom electrically neutral?",
        "type": "multiple_choice", 
        "options": [
            "It has only neutrons",
            "Number of protons equals number of electrons",
            "It has no charged particles",
            "Protons and neutrons cancel each other"
        ],
        "correct_answer": 1,
        "explanation": "An atom is neutral because it has equal numbers of positively charged protons and negatively charged electrons, so the charges cancel out.",
        "expected_output": ["B"]
    },
    {
        "id": 104,
        "name": "Valence Shell",
        "level": "Basic",
        "question": "The outermost shell of an atom is called:",
        "type": "multiple_choice",
        "options": [
            "Nucleus",
            "Valence shell", 
            "Core shell",
            "Proton shell"
        ],
        "correct_answer": 1,
        "explanation": "The outermost shell of an atom is called the valence shell. The number of electrons in this shell determines the atom's chemical properties.",
        "expected_output": ["B"]
    },
    {
        "id": 105,
        "name": "Diatomic Molecules",
        "level": "Basic",
        "question": "Which of these is a diatomic molecule (contains 2 atoms)?",
        "type": "multiple_choice",
        "options": [
            "Oxygen gas (O₂)",
            "Phosphorus (P₄)",
            "Glucose",
            "Argon (Ar)"
        ],
        "correct_answer": 0,
        "explanation": "O₂ (oxygen gas) is diatomic as it contains 2 oxygen atoms. Ar is monatomic, P₄ is tetratomic, and glucose is polyatomic.",
        "expected_output": ["A"]
    },
    {
        "id": 106,
        "name": "Electron Charge",
        "level": "Intermediate",
        "question": "Complete the sentence: The negatively charged particle of an atom is called __________.",
        "type": "fill_blank",
        "correct_answer": "electron",
        "explanation": "Electrons are the negatively charged particles that orbit around the nucleus of an atom.",
        "expected_output": ["electron"]
    },
    {
        "id": 107,
        "name": "Sodium Ion Formation",
        "level": "Intermediate", 
        "question": "Complete the sentence: Sodium forms a __________ ion by losing one electron.",
        "type": "fill_blank",
        "correct_answer": "positive",
        "explanation": "When sodium loses an electron, it has more protons than electrons, making it a positive ion (Na⁺) called a cation.",
        "expected_output": ["positive"]
    },
    {
        "id": 108,
        "name": "Ozone Atomicity",
        "level": "Intermediate",
        "question": "Complete the sentence: The molecule of ozone (O₃) is __________atomic.",
        "type": "fill_blank",
        "correct_answer": "tri",
        "explanation": "Ozone (O₃) contains 3 oxygen atoms, so it is triatomic.",
        "expected_output": ["tri"]
    },
    {
        "id": 109,
        "name": "Neutron Properties",
        "level": "Intermediate",
        "question": "True or False: Neutrons are positively charged particles.",
        "type": "true_false",
        "correct_answer": False,
        "explanation": "Neutrons are neutral particles with no electric charge. Protons are positively charged, and electrons are negatively charged.",
        "expected_output": ["False"]
    },
    {
        "id": 110,
        "name": "Water Molecule",
        "level": "Intermediate",
        "question": "True or False: Water (H₂O) is a molecule of a compound.",
        "type": "true_false", 
        "correct_answer": True,
        "explanation": "Water (H₂O) is a compound because it contains atoms of different elements (hydrogen and oxygen) chemically combined.",
        "expected_output": ["True"]
    },
    {
        "id": 111,
        "name": "Particle Matching",
        "level": "Intermediate",
        "question": "Match the atomic particles with their charges:\n1. Proton\n2. Neutron\n3. Electron\n\nOptions:\na) Neutral particle\nb) Negatively charged\nc) Positively charged\n\nEnter your answers as: 1-c, 2-a, 3-b",
        "type": "matching",
        "correct_answer": "1-c, 2-a, 3-b",
        "explanation": "Protons are positively charged, neutrons are neutral (no charge), and electrons are negatively charged.",
        "expected_output": ["1-c, 2-a, 3-b"]
    },
    {
        "id": 112,
        "name": "Types of Molecules",
        "level": "Intermediate",
        "question": "Classify these molecules by their atomicity:\nO₂, Ar, H₂O, P₄\n\nChoose the correct classification:",
        "type": "multiple_choice",
        "options": [
            "O₂: diatomic, Ar: monatomic, H₂O: triatomic, P₄: tetratomic",
            "O₂: monatomic, Ar: diatomic, H₂O: tetratomic, P₄: triatomic", 
            "O₂: triatomic, Ar: tetratomic, H₂O: monatomic, P₄: diatomic",
            "All are diatomic"
        ],
        "correct_answer": 0,
        "explanation": "O₂ has 2 atoms (diatomic), Ar has 1 atom (monatomic), H₂O has 3 atoms (triatomic), P₄ has 4 atoms (tetratomic).",
        "expected_output": ["A"]
    },
    {
        "id": 113,
        "name": "Sodium Chloride Formation",
        "level": "Advanced",
        "question": "Why does sodium (Na) combine with chlorine (Cl) to form NaCl? Explain in terms of electron transfer.",
        "type": "short_answer",
        "correct_answer": "Sodium has 1 electron in its valence shell and wants to lose it to become stable. Chlorine has 7 electrons in its valence shell and wants to gain 1 electron to complete its octet. Sodium transfers its electron to chlorine, forming Na⁺ and Cl⁻ ions, which attract each other to form NaCl.",
        "explanation": "Atoms combine to achieve stable electron configurations. Sodium loses 1 electron to form Na⁺, chlorine gains 1 electron to form Cl⁻, and opposite charges attract.",
        "expected_output": ["electron transfer", "stable", "Na+", "Cl-", "attract"]
    },
    {
        "id": 114,
        "name": "Magnesium Chloride Formula",
        "level": "Advanced",
        "question": "Write the steps to form the chemical formula of magnesium chloride:\n\nStep 1: Write symbols and charges\nStep 2: Determine valencies\nStep 3: Interchange valencies\nStep 4: Simplify\n\nWhat is the final formula?",
        "type": "short_answer",
        "correct_answer": "Step 1: Mg²⁺ and Cl⁻\nStep 2: Mg has valency 2, Cl has valency 1\nStep 3: Mg₁Cl₂\nStep 4: MgCl₂",
        "explanation": "Magnesium forms Mg²⁺ ions and chlorine forms Cl⁻ ions. To balance charges, we need 2 chlorine ions for each magnesium ion, giving MgCl₂.",
        "expected_output": ["MgCl₂", "Mg2+", "Cl-", "valency"]
    },
    {
        "id": 115,
        "name": "Oxygen Stability",
        "level": "Advanced", 
        "question": "Oxygen has 6 electrons in its valence shell. Explain how it achieves stability when reacting with calcium.",
        "type": "short_answer",
        "correct_answer": "Oxygen needs 2 more electrons to complete its valence shell (octet). Calcium has 2 electrons in its valence shell that it wants to lose. Calcium transfers its 2 electrons to oxygen, forming Ca²⁺ and O²⁻ ions. This gives oxygen 8 electrons in its valence shell, making it stable.",
        "explanation": "Atoms are stable when their valence shell is complete (8 electrons for most atoms). Oxygen gains electrons from calcium to achieve this stable configuration.",
        "expected_output": ["2 electrons", "octet", "Ca2+", "O2-", "stable", "8 electrons"]
    },
    {
        "id": 116,
        "name": "Ion Formation",
        "level": "Advanced",
        "question": "What are ions and how are they formed? Give examples of cations and anions.",
        "type": "short_answer",
        "correct_answer": "Ions are charged atoms formed when atoms lose or gain electrons. Cations are positively charged ions formed when atoms lose electrons (examples: Na⁺, Ca²⁺). Anions are negatively charged ions formed when atoms gain electrons (examples: Cl⁻, O²⁻).",
        "explanation": "Ions form when atoms gain or lose electrons to achieve stable electron configurations. The charge depends on whether electrons are gained or lost.",
        "expected_output": ["charged atoms", "lose electrons", "gain electrons", "cations", "anions", "Na+", "Cl-"]
    },
    {
        "id": 117,
        "name": "Compound Formation",
        "level": "Advanced",
        "question": "How do compounds form from ions? Explain with an example.",
        "type": "short_answer", 
        "correct_answer": "Compounds form when cations (positive ions) and anions (negative ions) attract each other due to opposite charges. For example, in NaCl, Na⁺ cations are attracted to Cl⁻ anions, forming an ionic compound through electrostatic attraction.",
        "explanation": "Ionic compounds form through the attraction between oppositely charged ions. This electrostatic attraction holds the compound together.",
        "expected_output": ["cations", "anions", "attract", "opposite charges", "electrostatic", "NaCl"]
    },
    {
        "id": 118,
        "name": "Atomic Structure Components", 
        "level": "Basic",
        "question": "An atom consists of three main types of particles. Which particles are found in the nucleus?",
        "type": "multiple_choice",
        "options": [
            "Protons and electrons",
            "Protons and neutrons", 
            "Neutrons and electrons",
            "Only protons"
        ],
        "correct_answer": 1,
        "explanation": "The nucleus of an atom contains protons (positively charged) and neutrons (neutral). Electrons orbit around the nucleus in shells.",
        "expected_output": ["B"]
    },
    {
        "id": 119,
        "name": "Valency and Chemical Bonding",
        "level": "Advanced",
        "question": "What is valency and how does it depend on electrons in the valence shell?",
        "type": "short_answer",
        "correct_answer": "Valency is the combining capacity of an element, determined by the number of electrons an atom can lose, gain, or share to achieve a stable electron configuration. It depends on the number of electrons in the valence shell - atoms with 1-3 valence electrons tend to lose them, while atoms with 5-7 valence electrons tend to gain electrons.",
        "explanation": "Valency determines how atoms combine with other atoms. It's based on achieving a stable electron configuration, usually 8 electrons in the valence shell.",
        "expected_output": ["combining capacity", "valence shell", "lose", "gain", "share", "stable"]
    },
    {
        "id": 120,
        "name": "Molecule vs Compound",
        "level": "Intermediate",
        "question": "What is the difference between a molecule of an element and a molecule of a compound?",
        "type": "short_answer",
        "correct_answer": "A molecule of an element contains only one type of atom (like O₂, Cl₂), while a molecule of a compound contains atoms of different elements chemically combined (like H₂O, CO₂).",
        "explanation": "Elements form molecules with identical atoms, while compounds form molecules with different types of atoms combined together.",
        "expected_output": ["one type", "different elements", "O₂", "H₂O", "chemically combined"]
    }
] 