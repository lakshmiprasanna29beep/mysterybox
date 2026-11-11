import sqlite3
from database import get_db_connection, init_db

def seed():
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    # =========================================================
    # CASE 1: The Stolen Blue Diamond (Super Simple English)
    # =========================================================
    cursor.execute("""
    INSERT INTO cases (id, title, tagline, difficulty, case_number, location, incident_time, victim, victim_role, briefing, incident_summary, icon, badge_color)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "case_sapphire",
        "Case 1: The Stolen Blue Diamond",
        "A huge blue diamond was stolen from a locked safe during a birthday party.",
        "Easy",
        "CASE #01",
        "Blackwood House, England",
        "11:45 PM at night (Raining)",
        "Mr. Blackwood",
        "Rich House Owner",
        "Tonight was Mr. Blackwood's 60th birthday party. At midnight, he went to his private room and saw that his big metal safe was wide open. His $4,000,000 blue diamond was gone! The guard dogs outside were put to sleep with medicine. The safe was not broken with tools—someone used a copied key. Four people in the house are suspects.",
        "The diamond is missing. The guard dogs outside are asleep. The person who stole it used a copied key and walked outside in the rain.",
        "fa-gem",
        "#3b82f6"
    ))

    # Crime scenes for Case 1
    cursor.executemany("""
    INSERT INTO crime_scenes (id, case_id, name, description, icon)
    VALUES (?, ?, ?, ?, ?)
    """, [
        ("scene_vault", "case_sapphire", "The Office & Safe Room", "The room where the big metal safe is kept. The safe door is open and empty.", "fa-vault"),
        ("scene_kennel", "case_sapphire", "The Dog Yard", "The place where two guard dogs are sleeping after eating drugged meat.", "fa-dog"),
        ("scene_gallery", "case_sapphire", "The Art Painting Room", "A big room with paintings on the walls and a glass door leading to the garden.", "fa-palette"),
        ("scene_pantry", "case_sapphire", "The Kitchen & Wine Room", "The back room where the house helper cleans plates and bottles.", "fa-utensils")
    ])

    # Suspects for Case 1
    cursor.executemany("""
    INSERT INTO suspects (id, case_id, name, role, age, avatar_svg, bio, initial_statement, motive_hint, alibi_claim, is_culprit, confession, innocent_statement)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            "suspect_james",
            "case_sapphire",
            "James (The Butler)",
            "House Helper & Butler",
            54,
            "butler",
            "He has worked in the house for 20 years. He has the house keys and serves food and wine.",
            "I was in the kitchen cleaning wine bottles the whole evening, Detective. Other helpers saw me.",
            "He owes money to money-lenders.",
            "Claims he was in the kitchen and wine cellar from 11:15 PM to 11:50 PM.",
            0,
            "",
            "I am telling the truth! I took a small amount of money last month because I owed debts, but I never stole the big diamond!"
        ),
        (
            "suspect_yvonne",
            "case_sapphire",
            "Madame Yvonne (French Guest)",
            "Art Dealer from Paris",
            42,
            "art_dealer",
            "A guest from Paris, France. She buys and sells expensive jewels and art.",
            "I was sitting alone in the Art Room looking at the nice paintings with a glass of juice. I saw nobody.",
            "Police know she sells stolen jewels in Europe for millions of dollars.",
            "Claims she sat alone in the Art Room looking at paintings between 11:30 PM and midnight.",
            1,
            "Okay, okay! You caught me! Mr. Blackwood didn't deserve that diamond anyway! A buyer in Europe promised me 4 million dollars for it! I copied the safe key using wax, gave sleeping medicine to the dogs, and took the diamond. I was going to catch the 4:30 AM morning train back to Paris!",
            ""
        ),
        (
            "suspect_julian",
            "case_sapphire",
            "Julian (The Nephew)",
            "Mr. Blackwood's Nephew",
            28,
            "nephew",
            "He is Mr. Blackwood's nephew. His uncle stopped giving him money last month.",
            "My uncle is mean to me. I was outside in the garden smoking in the rain.",
            "He needs money quickly to pay off debts.",
            "Claims he was outside in the rain between 11:35 PM and 11:55 PM.",
            0,
            "",
            "Look, I snuck into the office earlier to find my uncle's papers, but I heard a sound, got scared, dropped my lighter, and ran outside! I didn't open the safe!"
        ),
        (
            "suspect_vivienne",
            "case_sapphire",
            "Vivienne (Party Guest)",
            "Rich Guest at the Party",
            36,
            "socialite",
            "A rich lady attending the party. Her grandfather once owned this diamond many years ago.",
            "I was inside the big party hall dancing with friends. Everyone saw my shiny dress.",
            "She wanted the diamond back in her family.",
            "Claims she was dancing inside the party hall the whole time.",
            0,
            "",
            "I was dancing in the hall with twenty other people! I would never go out into the muddy rain in my expensive dress!"
        )
    ])

    # Clues for Case 1
    cursor.executemany("""
    INSERT INTO clues (id, case_id, scene_id, title, category, short_desc, full_analysis, icon, is_key_evidence)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            "clue_vault_dial",
            "case_sapphire",
            "scene_vault",
            "Safe Handle with Purple Makeup",
            "Physical",
            "The safe door was opened cleanly without breaking it. There is makeup on the handle.",
            "The safe was opened with a copied key. There is purple lipstick/makeup and soft wax inside the keyhole.",
            "fa-lock",
            1
        ),
        (
            "clue_drugged_meat",
            "case_sapphire",
            "scene_kennel",
            "Meat with French Sleeping Medicine",
            "Forensic",
            "Pieces of meat found near the sleeping guard dogs.",
            "The meat was soaked in a sleeping medicine called 'Valériane'. This medicine is only sold in Paris, France pharmacies.",
            "fa-flask",
            1
        ),
        (
            "clue_cigar_lighter",
            "case_sapphire",
            "scene_vault",
            "Julian's Silver Lighter",
            "Physical",
            "A small lighter found under the carpet in the office.",
            "The lighter has the letters 'J.B.' for Julian Blackwood. It was dropped by accident.",
            "fa-fire",
            0
        ),
        (
            "clue_terrace_mud",
            "case_sapphire",
            "scene_gallery",
            "Muddy Footprints & Purple Dress Thread",
            "Physical",
            "Wet footprints from the garden with a thread of purple cloth.",
            "Small shoe prints (women's size 38). A piece of purple silk thread from a woman's party dress was caught on the rose bushes outside.",
            "fa-shoe-prints",
            1
        ),
        (
            "clue_wine_inventory",
            "case_sapphire",
            "scene_pantry",
            "Kitchen Work Logbook",
            "Document",
            "The helper's book with notes showing his work in the kitchen all night.",
            "James wrote entries at 11:20, 11:35, and 11:48 PM while opening wine bottles. Kitchen helpers confirmed he was there.",
            "fa-book-open",
            0
        ),
        (
            "clue_wax_impression",
            "case_sapphire",
            "scene_gallery",
            "Wax Piece with Key Shape",
            "Forensic",
            "A piece of wax found hidden behind a statue in the Art Room.",
            "The wax has the exact shape of the safe key! It smells like lavender hand cream.",
            "fa-fingerprint",
            1
        ),
        (
            "clue_train_ticket",
            "case_sapphire",
            "scene_pantry",
            "Early Train Ticket to Paris (4:30 AM)",
            "Document",
            "A train ticket found in a woman's handbag left near the coat rack.",
            "A one-way morning train ticket to Paris leaving at 4:30 AM under the name 'Y. Delacroix' (Madame Yvonne). The bag smells of lavender cream and has purple makeup.",
            "fa-ticket",
            1
        )
    ])

    # Dialogues for Case 1 (Simple English)
    cursor.executemany("""
    INSERT INTO suspect_dialogues (suspect_id, topic, question, answer, reaction_mood, unlocks_clue_id)
    VALUES (?, ?, ?, ?, ?, ?)
    """, [
        # James
        ("suspect_james", "Where were you?", "Can someone confirm you were in the kitchen all night?", "Yes! The other kitchen helpers saw me opening wine bottles. I wrote down every bottle in my kitchen logbook.", "calm", "clue_wine_inventory"),
        ("suspect_james", "Safe Key", "Who had access to the safe key?", "Mr. Blackwood had it in his coat. But during dinner, he hung his coat in the coat rack where guests also put their coats and bags.", "nervous", None),
        ("suspect_james", "The Dogs", "Did you feed the dogs meat?", "No, I only feed them dry food. I never gave them meat or sleeping pills.", "calm", None),

        # Yvonne
        ("suspect_yvonne", "Art Room", "You said you were looking at paintings alone?", "Yes, I was sitting alone looking at the beautiful paintings between 11:30 and midnight. Nobody was with me.", "smug", None),
        ("suspect_yvonne", "Sleeping Medicine", "Do you know about this French sleeping medicine given to the dogs?", "Sleeping medicine? No! I am an art dealer, not a doctor. I do not carry dog medicines.", "nervous", None),
        ("suspect_yvonne", "Travel Plans", "When are you going back home to Paris?", "Oh, in a few days. I have not booked any train ticket yet. I like London.", "smug", None),

        # Julian
        ("suspect_julian", "In the Office", "We found your lighter in the office, Julian.", "Okay, I went in at 10:30 PM to find my uncle's papers, but I heard footsteps, got scared, dropped my lighter, and ran outside!", "nervous", None),
        ("suspect_julian", "In the Rain", "Who saw you outside in the garden?", "Nobody, it was raining! But look at my shoes, they are completely wet from the mud in the garden.", "angry", None),

        # Vivienne
        ("suspect_vivienne", "Dancing", "Did you go outside into the garden in the rain?", "In this expensive silk dress? Never! The rain would ruin my dress. I stayed in the warm party hall.", "calm", None),
        ("suspect_vivienne", "The Diamond", "Do you dislike Mr. Blackwood?", "He is not very nice, but I would never steal anything. Stealing is wrong.", "smug", None)
    ])

    # Contradictions for Case 1 (Simple English)
    cursor.executemany("""
    INSERT INTO contradictions (suspect_id, clue_id, callout_text, suspect_response, breaks_alibi)
    VALUES (?, ?, ?, ?, ?)
    """, [
        (
            "suspect_yvonne",
            "clue_train_ticket",
            "You said you did not book a ticket to Paris, but we found a 4:30 AM morning train ticket with your name 'Y. Delacroix' inside your lavender handbag!",
            "W-what?! That... that was just a backup ticket in case the party got boring!",
            1
        ),
        (
            "suspect_yvonne",
            "clue_terrace_mud",
            "You said you stayed inside the Art Room, but we found purple dress threads matching your dress on the garden bushes, and muddy footprints size 38!",
            "Oh no... I... I just stepped outside for a second to get fresh air!",
            1
        ),
        (
            "suspect_yvonne",
            "clue_drugged_meat",
            "The dogs were put to sleep with a special medicine sold only in Paris, France—where you just came from!",
            "Many people go to Paris! That doesn't prove it was me!",
            1
        ),
        (
            "suspect_yvonne",
            "clue_vault_dial",
            "Your purple makeup was found right on the metal handle of the safe, and wax was inside the keyhole!",
            "My makeup?! How did that get there...",
            1
        ),
        (
            "suspect_james",
            "clue_wine_inventory",
            "Your kitchen logbook and kitchen helpers confirm you were opening wine bottles the whole time.",
            "Yes, Detective! That proves I was doing my job in the kitchen.",
            0
        )
    ])

    # Case 1 Solution (Simple English)
    cursor.execute("""
    INSERT INTO case_solutions (case_id, culprit_suspect_id, weapon_clue_id, key_proof_clue_id, motive_summary, full_verdict_narrative)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "case_sapphire",
        "suspect_yvonne",
        "clue_wax_impression",
        "clue_train_ticket",
        "She wanted to take the diamond to Paris and sell it to a private buyer for 4 million dollars.",
        "Madame Yvonne took the safe key from Mr. Blackwood's coat while he was eating dinner, made a copy using soft wax, and put the key back. At 11:35 PM, she fed the guard dogs meat soaked in French sleeping medicine, opened the safe with her copied key, and stole the diamond. When police found her secret 4:30 AM train ticket to Paris, the wax key mold, and purple dress threads on the bushes, Madame Yvonne admitted her crime and was arrested!"
    ))

    # =========================================================
    # CASE 2: The Poisoned Tea (Super Simple English)
    # =========================================================
    cursor.execute("""
    INSERT INTO cases (id, title, tagline, difficulty, case_number, location, incident_time, victim, victim_role, briefing, incident_summary, icon, badge_color)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "case_sonata",
        "Case 2: The Poisoned Tea",
        "A music conductor drank his tea on stage and died from poison.",
        "Medium",
        "CASE #02",
        "Royal Concert Hall, London",
        "8:15 PM (Music Rehearsal)",
        "Arturo Vane",
        "Famous Music Conductor",
        "It was rehearsal night at the Royal Concert Hall. Conductor Arturo Vane lifted his usual cup of warm tea from the stand at center stage, took one sip, and fell. He was dead before help arrived. The doctor found cyanide in the tea. The honey jar in the tea room was clean, so the poison was poured into the cup itself after the tea was made. The hall doors were locked. Only four people backstage could have touched that cup: the violin player, the stage manager who carried the tea, the pianist, and the rich sponsor watching from upstairs.",
        "The conductor died from poison poured into his tea cup. Only the stage manager carried that cup to the stand.",
        "fa-music",
        "#8b5cf6"
    ))

    cursor.executemany("""
    INSERT INTO crime_scenes (id, case_id, name, description, icon)
    VALUES (?, ?, ?, ?, ?)
    """, [
        ("scene_podium", "case_sonata", "The Conductor Stage", "Center stage. Music stand knocked over and the half-empty tea cup on the table.", "fa-drum"),
        ("scene_greenroom", "case_sonata", "The Private Tea Room", "The dressing room where hot water, honey, and tea bags are kept.", "fa-couch"),
        ("scene_backstage", "case_sonata", "Backstage Lighting Desk", "The area behind the stage where stage helpers control lights and cables.", "fa-theater-masks"),
        ("scene_library", "case_sonata", "The Music Book Room", "A room filled with music books, papers, and files.", "fa-archive")
    ])

    cursor.executemany("""
    INSERT INTO suspects (id, case_id, name, role, age, avatar_svg, bio, initial_statement, motive_hint, alibi_claim, is_culprit, confession, innocent_statement)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            "suspect_elena",
            "case_sonata",
            "Elena (Violin Player)",
            "Chief Violinist",
            34,
            "violinist",
            "The top violin player. She often argued with the conductor about music.",
            "I was on stage tuning my violin with other musicians from 7:45 PM until the music started.",
            "The conductor threatened to fire her tomorrow.",
            "Claims she was sitting on stage tuning her violin.",
            0,
            "",
            "I disliked him because he was mean, but I am an artist! I would never poison anyone!"
        ),
        (
            "suspect_oliver",
            "case_sonata",
            "Oliver (Stage Manager)",
            "Stage Manager",
            48,
            "stage_manager",
            "He prepares the stage and always makes the conductor's tea every night.",
            "I made the conductor's tea at 7:40 PM, carried the cup to his stand at 7:55 PM, and went back to my lights.",
            "His daughter was a singer who died after the conductor was very cruel to her and ruined her career.",
            "Claims he never left the light controls after delivering the tea.",
            1,
            "He deserved it! He was so cruel to my sweet daughter that she took her own life! He ruined her dreams and laughed about it. I put the poison in his cup so he could never hurt anyone again!",
            ""
        ),
        (
            "suspect_clara_b",
            "case_sonata",
            "Clara (Piano Player)",
            "Young Pianist",
            25,
            "pianist",
            "A talented young pianist whose song was stolen by the conductor.",
            "I was in the basement room practicing piano with headphones on.",
            "The conductor stole her music song and took all the money.",
            "Claims she was practicing piano in the basement.",
            0,
            "",
            "I had a lawyer ready to take him to court next week to get my money back! If he dies, I can't get my money back easily!"
        ),
        (
            "suspect_marcus",
            "case_sonata",
            "Marcus (Rich Sponsor)",
            "Hall Sponsor",
            59,
            "patron",
            "A wealthy businessman who gives money to the music hall.",
            "I was sitting upstairs in the private box watching the rehearsal.",
            "The conductor found out Marcus was stealing money from the hall funds.",
            "Claims he was upstairs in the VIP box.",
            0,
            "",
            "The conductor was asking me for money, but I would never kill someone in front of a whole orchestra!"
        )
    ])

    cursor.executemany("""
    INSERT INTO clues (id, case_id, scene_id, title, category, short_desc, full_analysis, icon, is_key_evidence)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            "clue_spiked_mug",
            "case_sonata",
            "scene_podium",
            "Poisoned Tea Cup",
            "Forensic",
            "The conductor's tea cup found on stage with poison inside.",
            "Lab tests found deadly white cyanide poison mixed directly into the tea.",
            "fa-mug-hot",
            1
        ),
        (
            "clue_honey_dipper",
            "case_sonata",
            "scene_greenroom",
            "Clean Honey Jar",
            "Forensic",
            "The honey jar in the kitchen used for making the tea.",
            "The honey jar is completely clean and safe. The poison was added directly into the cup later, not from the honey jar.",
            "fa-jar",
            1
        ),
        (
            "clue_photo_locket",
            "case_sonata",
            "scene_backstage",
            "Silver Locket with Poison Powder",
            "Document",
            "A silver necklace locket found dropped under Oliver's lighting desk.",
            "Inside is a photo of Oliver's daughter Clara. Tucked inside is a paper packet with white cyanide poison powder!",
            "fa-portrait",
            1
        ),
        (
            "clue_stage_cue_sheet",
            "case_sonata",
            "scene_backstage",
            "Stage Duty Sheet",
            "Document",
            "Oliver's clipboard showing what time he carried the tea.",
            "Notes show: '7:50 PM - Made tea. 7:55 PM - Hand-delivered tea to stage.' Only Oliver touched the cup.",
            "fa-clipboard-list",
            1
        ),
        (
            "clue_violins_scoresheet",
            "case_sonata",
            "scene_podium",
            "Marked Music Sheet",
            "Document",
            "The conductor's paper sheets with mean notes written in red.",
            "Mean notes written about the violin section: 'Elena plays poorly. Replace her soon.'",
            "fa-file-signature",
            0
        )
    ])

    cursor.executemany("""
    INSERT INTO suspect_dialogues (suspect_id, topic, question, answer, reaction_mood, unlocks_clue_id)
    VALUES (?, ?, ?, ?, ?, ?)
    """, [
        ("suspect_oliver", "Making the Tea", "Did anyone else touch the tea after you made it?", "Nobody. I made it in the tea room, carried it straight to his stand at 7:55 PM, and left.", "calm", "clue_stage_cue_sheet"),
        ("suspect_oliver", "Your Daughter", "Did your daughter sing here before?", "My... my daughter passed away a few years ago. Please don't talk about her.", "nervous", None),
        ("suspect_elena", "Arguments", "Did the conductor threaten to replace you?", "He always shouted at people, but I wouldn't kill him for that.", "calm", None),
        ("suspect_clara_b", "Stolen Song", "Did the conductor take your song?", "Yes, but I was taking him to court next week with my lawyer.", "calm", None)
    ])

    cursor.executemany("""
    INSERT INTO contradictions (suspect_id, clue_id, callout_text, suspect_response, breaks_alibi)
    VALUES (?, ?, ?, ?, ?)
    """, [
        (
            "suspect_oliver",
            "clue_photo_locket",
            "We found your silver locket under your desk with your daughter's photo and white cyanide poison powder inside!",
            "My... my daughter's locket! You don't know the sadness he caused her!",
            1
        ),
        (
            "suspect_oliver",
            "clue_honey_dipper",
            "The honey jar was completely clean! The poison was dropped into the cup while only YOU carried it to the stage!",
            "I... someone else could have walked by!",
            1
        ),
        (
            "suspect_oliver",
            "clue_stage_cue_sheet",
            "Your own duty sheet shows you carried the cup directly to the stage 5 minutes before he drank it!",
            "He deserved it! He drove my child to suicide!",
            1
        )
    ])

    cursor.execute("""
    INSERT INTO case_solutions (case_id, culprit_suspect_id, weapon_clue_id, key_proof_clue_id, motive_summary, full_verdict_narrative)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "case_sonata",
        "suspect_oliver",
        "clue_spiked_mug",
        "clue_photo_locket",
        "He wanted revenge because the conductor was very mean to his daughter, causing her suicide.",
        "Stage manager Oliver Finch poisoned the conductor's tea because the conductor had cruelly ruined his daughter's career. When police found his daughter's locket with poison powder and proved only he held the tea cup, Oliver broke down and admitted his guilt."
    ))

    # =========================================================
    # CASE 3: The Stolen Computer Chip (Super Simple English)
    # =========================================================
    cursor.execute("""
    INSERT INTO cases (id, title, tagline, difficulty, case_number, location, incident_time, victim, victim_role, briefing, incident_summary, icon, badge_color)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "case_cyber",
        "Case 3: The Stolen Computer Chip",
        "A scientist was found unconscious in a cold server room, and a chip was stolen.",
        "Hard",
        "CASE #03",
        "Tech Lab Server Room, Cambridge",
        "2:15 AM (Night Shift)",
        "Dr. Aris",
        "Chief Computer Scientist",
        "At 2:15 AM the alarm went off in the cold server vault at the Cambridge tech lab. Dr. Aris, the chief scientist, was lying unconscious on the floor. Someone had flipped the red emergency gas switch and knocked him out. The glass case in the middle of the room was smashed, and the secret AI computer chip was gone. The security cameras showed an old loop of video, so they never recorded who walked in. Only four people were inside the building: the engineer, the security guard, the cooling technician, and the company boss.",
        "Dr. Aris was knocked out with gas, the cameras were frozen, and the secret computer chip was stolen.",
        "fa-microchip",
        "#10b981"
    ))

    cursor.executemany("""
    INSERT INTO crime_scenes (id, case_id, name, description, icon)
    VALUES (?, ?, ?, ?, ?)
    """, [
        ("scene_q_vault", "case_cyber", "The Cold Server Room", "The cold room where computer servers and secret chips are kept.", "fa-server"),
        ("scene_security_hub", "case_cyber", "Security Desk", "Monitors and security camera screens.", "fa-shield-halved"),
        ("scene_airlock", "case_cyber", "The Locker Room", "Suits and storage lockers for lab workers.", "fa-door-closed"),
        ("scene_lab_office", "case_cyber", "The Scientist Office", "Desk with computer papers and coffee cups.", "fa-laptop-code")
    ])

    cursor.executemany("""
    INSERT INTO suspects (id, case_id, name, role, age, avatar_svg, bio, initial_statement, motive_hint, alibi_claim, is_culprit, confession, innocent_statement)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            "suspect_sarah",
            "case_cyber",
            "Dr. Sarah (Engineer)",
            "Lead Algorithm Engineer",
            32,
            "engineer",
            "The second scientist in the lab. She wanted a promotion.",
            "I was testing computer programs on computer 4 the whole time until the sirens rang.",
            "She wanted more credit for the research.",
            "Claims she was sitting at computer 4 in the dry lab.",
            0,
            "",
            "I helped build that computer chip! I would never destroy my own hard work!"
        ),
        (
            "suspect_viktor",
            "case_cyber",
            "Viktor (Security Guard)",
            "Head Security Officer",
            46,
            "security",
            "The security guard who controls the doors, keys, and cameras.",
            "I was sitting at the front desk watching cameras. Nobody walked in.",
            "He needed millions of dollars to pay off big debts.",
            "Claims he never left the front camera desk.",
            1,
            "A foreign company offered me 15 million dollars to steal that computer drive! Dr. Aris walked in while I was copying the files. I panicked, turned on the emergency gas switch to knock him out, and ran! You got me!",
            ""
        ),
        (
            "suspect_maya",
            "case_cyber",
            "Maya (Fix-it Technician)",
            "Cooling Pipe Technician",
            27,
            "sysadmin",
            "A worker who fixes cooling pipes in the building.",
            "I was under the pipes fixing a water leak with my wrench.",
            "She wrote complaints about bad safety rules.",
            "Claims she was under the floor pipes working.",
            0,
            "",
            "I told everyone that the emergency gas switch had no password! I warned them weeks ago!"
        ),
        (
            "suspect_grant",
            "case_cyber",
            "Harrison (The Boss / COO)",
            "Company Manager",
            52,
            "ceo",
            "The rich company manager.",
            "I was upstairs in my office on a phone call with investors.",
            "The company was in trouble for test numbers.",
            "Claims he stayed upstairs in his office.",
            0,
            "",
            "If that chip is stolen, our company loses all its value! Why would I ruin my own company?!"
        )
    ])

    cursor.executemany("""
    INSERT INTO clues (id, case_id, scene_id, title, category, short_desc, full_analysis, icon, is_key_evidence)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            "clue_nitrogen_purge",
            "case_cyber",
            "scene_q_vault",
            "The Emergency Gas Switch",
            "Forensic",
            "The wall switch that released gas into the room.",
            "Fingerprint powder found Viktor the Security Guard's fingerprint right on the red gas switch!",
            "fa-wind",
            1
        ),
        (
            "clue_cloned_keycard",
            "case_cyber",
            "scene_security_hub",
            "Fake Camera Looper Device",
            "Physical",
            "A small device hidden behind the security desk fan.",
            "It repeated an old 15-second video so the camera wouldn't show Viktor walking into the server room.",
            "fa-id-card",
            1
        ),
        (
            "clue_drive_shredder",
            "case_cyber",
            "scene_airlock",
            "The Stolen Drive in an Oxygen Tank",
            "Physical",
            "The stolen computer drive hidden inside a hollow oxygen tank in the locker.",
            "The locker belongs to Viktor the security guard. The secret files were copied onto this drive.",
            "fa-hard-drive",
            1
        ),
        (
            "clue_bank_ledger",
            "case_cyber",
            "scene_security_hub",
            "Secret Bank Deposit Alert",
            "Document",
            "A printed bank paper found under the desk printer.",
            "Shows 2.5 million dollars sent to Viktor's secret overseas bank account.",
            "fa-file-invoice-dollar",
            1
        )
    ])

    cursor.executemany("""
    INSERT INTO suspect_dialogues (suspect_id, topic, question, answer, reaction_mood, unlocks_clue_id)
    VALUES (?, ?, ?, ?, ?, ?)
    """, [
        ("suspect_viktor", "Camera Video", "Why did the camera freeze at 2:00 AM?", "Oh, the computer was doing a routine backup, that is normal.", "calm", "clue_cloned_keycard"),
        ("suspect_viktor", "Gas Switch", "Did you touch the red gas switch?", "No, never! I stayed in my chair.", "nervous", None),
        ("suspect_viktor", "Money", "Did someone send you money recently?", "No, I only get my normal salary.", "angry", "clue_bank_ledger"),
        ("suspect_sarah", "Working Together", "Did you like Dr. Aris?", "Yes, he was my teacher and friend. I would never hurt him.", "calm", None)
    ])

    cursor.executemany("""
    INSERT INTO contradictions (suspect_id, clue_id, callout_text, suspect_response, breaks_alibi)
    VALUES (?, ?, ?, ?, ?)
    """, [
        (
            "suspect_viktor",
            "clue_nitrogen_purge",
            "You said you never touched the red gas switch, but your fingerprint was found right on it!",
            "I... I might have cleaned it earlier! That proves nothing!",
            1
        ),
        (
            "suspect_viktor",
            "clue_cloned_keycard",
            "We found this camera looper device hidden in your desk that froze the cameras so you could sneak inside!",
            "Where did you find that?! Someone put that in my desk!",
            1
        ),
        (
            "suspect_viktor",
            "clue_bank_ledger",
            "A secret bank alert shows 2.5 million dollars sent to your overseas account for the stolen chip!",
            "Darn it... you checked my bank records!",
            1
        )
    ])

    cursor.execute("""
    INSERT INTO case_solutions (case_id, culprit_suspect_id, weapon_clue_id, key_proof_clue_id, motive_summary, full_verdict_narrative)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "case_cyber",
        "suspect_viktor",
        "clue_nitrogen_purge",
        "clue_drive_shredder",
        "He wanted to sell the secret computer drive to a foreign buyer for 15 million dollars.",
        "Security guard Viktor used a camera looper device to hide his steps, snuck into the server room, and copied the secret drive. When Dr. Aris surprised him, Viktor flipped the gas switch to knock him out and hid the stolen drive in an oxygen tank. Confronted with his fingerprints, the fake camera device, and the stolen drive, Viktor surrendered to police."
    ))

    conn.commit()
    conn.close()
    print("Database successfully re-seeded with Simple, Clear English!")

if __name__ == "__main__":
    seed()
