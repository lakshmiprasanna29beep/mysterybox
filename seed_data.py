import sqlite3
from database import get_db_connection, init_db

def seed():
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    # ==========================================
    # CASE 1: The Blackwood Sapphire Heist
    # ==========================================
    cursor.execute("""
    INSERT INTO cases (id, title, tagline, difficulty, case_number, location, incident_time, victim, victim_role, briefing, incident_summary, icon, badge_color)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "case_sapphire",
        "The Blackwood Sapphire Heist",
        "A 150-carat royal jewel vanished from a high-security manor vault mid-gala.",
        "Intermediate",
        "CASE-084-A",
        "Blackwood Estate, Surrey, England",
        "11:45 PM, Rainy Gala Night",
        "Lord Percival Blackwood",
        "Collector & Aristocrat",
        "During Lord Blackwood's 60th birthday masquerade gala, the priceless 'Eye of Osiris' sapphire vanished from his personal steel vault. The vault required both a mechanical combination dial and a unique brass master key. The guard dogs outside were found asleep, and no windows were shattered. All four suspects were present in the manor at the time of the theft.",
        "The stolen gem is worth over £4,000,000. Lord Blackwood discovered the vault wide open at midnight. The private guard dogs were peacefully tranquilized. Rain was pouring outside, meaning anyone leaving the manor grounds would have tracking mud.",
        "fa-gem",
        "#3b82f6"
    ))

    # Crime scenes for Case 1
    cursor.executemany("""
    INSERT INTO crime_scenes (id, case_id, name, description, icon)
    VALUES (?, ?, ?, ?, ?)
    """, [
        ("scene_vault", "case_sapphire", "The Private Study & Vault", "Heavy mahogany bookshelves surround a heavy steel floor-vault. The door stands ajar.", "fa-vault"),
        ("scene_kennel", "case_sapphire", "The Guard Dog Kennels", "Two trained Dobermans are groggily recovering in their straw beds. Food bowls nearby.", "fa-dog"),
        ("scene_gallery", "case_sapphire", "The West Portrait Gallery", "Lined with antique paintings, French doors opening to the rainy garden terrace.", "fa-palette"),
        ("scene_pantry", "case_sapphire", "The Butler's Pantry", "A discreet backroom stacked with silver trays, decanters, and coat racks.", "fa-utensils")
    ])

    # Suspects for Case 1
    cursor.executemany("""
    INSERT INTO suspects (id, case_id, name, role, age, avatar_svg, bio, initial_statement, motive_hint, alibi_claim, is_culprit, confession, innocent_statement)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            "suspect_james",
            "case_sapphire",
            "James Thornton",
            "Head Butler",
            54,
            "butler",
            "Serving the Blackwood family for 22 years. Methodical, stiff-lipped, and trusted with the estate keys.",
            "I was overseeing the dessert service and inventorying the vintage Bordeaux in the pantry until 11:55 PM, Detective.",
            "Rumors suggest he has staggering gambling debts with London bookmakers.",
            "Claims he never left the basement cellar and pantry between 11:15 PM and 11:50 PM.",
            0,
            "",
            "I swear upon my mother's grave! I took five hundred pounds from the petty cash last month to stave off debt collectors, but I would never steal the master's jewel!"
        ),
        (
            "suspect_yvonne",
            "case_sapphire",
            "Madame Yvonne Delacroix",
            "Parisian Art Dealer",
            42,
            "art_dealer",
            "A charismatic and sharp international antiquities broker who traveled from Paris specifically for the gala.",
            "I was enchanted by Lord Blackwood's Flemish portraits in the West Gallery. I sat with a glass of champagne admiring the brushstrokes.",
            "Interpol suspects her gallery is a front for a high-end European jewel fencing ring.",
            "Claims she sat alone in the West Gallery from 11:30 PM to midnight admiring paintings.",
            1,
            "Fine! Save your grand lecture, Inspector. Percival Blackwood bought that stone from colonial smugglers for pennies! A private collector in Geneva was willing to pay four million euros in untraceable bearer bonds. If that idiot butler hadn't kept the vault combination hidden behind his silly chessboard, I wouldn't have even needed to copy Lord Blackwood's wax key imprint!",
            ""
        ),
        (
            "suspect_julian",
            "case_sapphire",
            "Julian Blackwood",
            "Estranged Nephew",
            28,
            "nephew",
            "A reckless spendthrift nephew who was publicly cut from Lord Blackwood's will three weeks ago.",
            "My uncle is a tyrant. I was out on the terrace having a smoke, freezing my fingers off, cursing his name.",
            "Desperate for cash to avoid prison over a failed maritime investment scheme.",
            "Claims he stood on the covered garden terrace smoking cigars between 11:35 PM and 11:55 PM.",
            0,
            "",
            "Look, I snuck into the study earlier that evening trying to find my uncle's will to burn it! But when I heard footsteps, I panicked and dropped my silver cigar lighter and bolted! I never opened the vault!"
        ),
        (
            "suspect_vivienne",
            "case_sapphire",
            "Lady Vivienne Vance",
            "Socialite & Rival Collector",
            36,
            "socialite",
            "Glamorous heiress whose family once owned the Eye of Osiris eighty years ago.",
            "I came to see the sapphire one last time. It was rightful family property before Percival swindled my grandfather.",
            "Wants the gem to restore her family's ancestral honor.",
            "Claims she was dancing in the main ballroom in full view of twenty guests.",
            0,
            "",
            "I was in the ballroom dancing the waltz! Ask anyone—my silver sequin gown was impossible to miss! I wanted the stone back legally, not through vulgar burglary!"
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
            "Clean Vault Dial & Scratches",
            "Physical",
            "The combination lock was opened with zero signs of explosive or drill tampering.",
            "Forensic light shows no forced entry on the dial. However, microscopic wax residue is embedded inside the keyhole, and a faint smear of violet cosmetic rouge was found on the brass handle.",
            "fa-lock",
            1
        ),
        (
            "clue_drugged_meat",
            "case_sapphire",
            "scene_kennel",
            "Raw Beef with Valerian Tincture",
            "Forensic",
            "Discarded pieces of prime steak found in the kennels, soaked in sedative liquid.",
            "Chemical residue tests positive for 'Valériane Somnifère'—a boutique French veterinary sedative sold exclusively through registered Parisian apothecary shops.",
            "fa-flask",
            1
        ),
        (
            "clue_cigar_lighter",
            "case_sapphire",
            "scene_vault",
            "Engraved Silver Cigar Lighter",
            "Physical",
            "Found tucked under the oriental rug right next to the study desk.",
            "The lighter bears the initials 'J.B.'—Julian Blackwood. It smells fresh, but the flint is jammed with lint.",
            "fa-fire",
            0
        ),
        (
            "clue_terrace_mud",
            "case_sapphire",
            "scene_gallery",
            "Muddy Footprints & Silk Hem",
            "Physical",
            "Faint damp shoe prints on the parquet leading in from the terrace French doors.",
            "Size 38 European (women's designer shoe). Snagged on the terrace rosebush is a thread of rare plum-colored French silk gauze.",
            "fa-shoe-prints",
            1
        ),
        (
            "clue_wine_inventory",
            "case_sapphire",
            "scene_pantry",
            "Cellar Inventory Logbook",
            "Document",
            "The butler's logbook with timestamped cellar checks throughout the evening.",
            "Shows entries written in James's penmanship at 11:20, 11:35, and 11:48 PM, with wet red wine rings on the table consistent with sustained decanting work.",
            "fa-book-open",
            0
        ),
        (
            "clue_wax_impression",
            "case_sapphire",
            "scene_gallery",
            "Discarded Wax Seal & Shavings",
            "Forensic",
            "Hidden behind a bust of Napoleon in the West Gallery: dental wax with a key impression.",
            "The mold perfectly matches Lord Blackwood's vault master key. Residue of high-end lavender hand lotion is dried on the wrapper.",
            "fa-fingerprint",
            1
        ),
        (
            "clue_train_ticket",
            "case_sapphire",
            "scene_pantry",
            "Early Eurostar Express Ticket",
            "Document",
            "Found inside a forgotten clutch left by the guest coat rack in the pantry.",
            "A one-way London St Pancras to Paris Gare du Nord ticket booked for 4:30 AM tomorrow under the name 'Y. Delacroix'. The bag smells distinctly of French lavender and violet cosmetic rouge.",
            "fa-ticket",
            1
        )
    ])

    # Dialogues for Case 1
    cursor.executemany("""
    INSERT INTO suspect_dialogues (suspect_id, topic, question, answer, reaction_mood, unlocks_clue_id)
    VALUES (?, ?, ?, ?, ?, ?)
    """, [
        # James dialogues
        ("suspect_james", "Whereabouts", "Can anyone corroborate that you remained in the cellar all evening?", "The scullery maid and footman saw me decanting the 1982 Château Margaux. My inventory log records every vintage brought up to the gala floor.", "calm", "clue_wine_inventory"),
        ("suspect_james", "The Vault Key", "Did anyone have access to the master key besides you and Lord Blackwood?", "Lord Blackwood keeps the key on his waistcoat chain. However, during dinner, he hung his formal coat in the parlor cloakroom where guests also placed their wraps.", "nervous", None),
        ("suspect_james", "The Dogs", "Did you feed the Dobermans tonight?", "Certainly not raw beef! The kennel master prepared dry kibble at 5 PM. I never use sedatives, Detective.", "neutral", None),

        # Yvonne dialogues
        ("suspect_yvonne", "Art Gallery", "You claimed you were admiring the Dutch portraits between 11:30 and midnight?", "Mais oui! The lighting on the Rembrandt replica in the West Gallery is exquisite at night. I didn't see or hear a soul.", "smug", None),
        ("suspect_yvonne", "French Sedative", "Do you recognize this French veterinary sedative found with the dogs?", "Veterinary medicine? Mon dieu, Inspector, I am a fine art curator, not a veterinarian! I carry perfume, not sleeping drugs.", "nervous", None),
        ("suspect_yvonne", "Travel Plans", "When do you plan to return to Paris?", "Oh, in a few days... I haven't even booked my return passage yet. I adore London in the autumn.", "smug", None),

        # Julian dialogues
        ("suspect_julian", "Study Intrusion", "We found your silver lighter on the study floor, Julian.", "All right! I'll confess! I went into Uncle's study at 10:30 PM trying to snatch his handwritten codicil to burn it. But I couldn't open his safe, heard someone coming, and fled through the conservatory!", "nervous", None),
        ("suspect_julian", "Alibi", "Who saw you out on the terrace at 11:45 PM?", "Nobody, it was raining cats and dogs! But check my dress shoes—they are soaked through and covered in garden soil!", "angry", None),

        # Vivienne dialogues
        ("suspect_vivienne", "Ballroom Presence", "Did you step outside into the garden terrace at any point?", "In this silk chiffon skirt? In the Surrey rain? Heavens no, I would ruin five thousand guineas of handmade couture!", "calm", None),
        ("suspect_vivienne", "The Sapphire", "Do you hold resentment towards Lord Blackwood?", "He is a pompous hoarder, but I am negotiating with his creditors to buy the estate in foreclosure. Theft is so terribly bourgeois.", "smug", None)
    ])

    # Contradictions for Case 1
    cursor.executemany("""
    INSERT INTO contradictions (suspect_id, clue_id, callout_text, suspect_response, breaks_alibi)
    VALUES (?, ?, ?, ?, ?)
    """, [
        (
            "suspect_yvonne",
            "clue_train_ticket",
            "You claimed you hadn't booked your return passage to Paris, yet we discovered a 4:30 AM Eurostar ticket in your name tucked away in your lavender-scented clutch!",
            "W-what? That... that was merely a provisional ticket in case the gala bored me!",
            1
        ),
        (
            "suspect_yvonne",
            "clue_terrace_mud",
            "You claimed you sat peacefully admiring paintings in the West Gallery, but the rosebush by the terrace door snagged a thread of plum French silk gauze matching your gown, alongside size 38 footprints!",
            "Sacré bleu... a woman cannot take some fresh midnight air without being interrogated?!",
            1
        ),
        (
            "suspect_yvonne",
            "clue_drugged_meat",
            "The guard dogs were poisoned with Valériane Somnifère—a specialized sedative compounded exclusively in Parisian pharmacies!",
            "You think you are clever, don't you?! Many people travel between Paris and London!",
            1
        ),
        (
            "suspect_yvonne",
            "clue_vault_dial",
            "Forensic analysis of the vault dial revealed your signature violet cosmetic rouge and traces of dental wax inside the keyhole!",
            "Mon dieu... my compact must have brushed the dial...",
            1
        ),
        (
            "suspect_james",
            "clue_wine_inventory",
            "Your cellar ledger confirms three separate decanting batches right during the window of the burglary, supported by kitchen staff testimony.",
            "Indeed, Detective. As I told you, duty keeps me at my station.",
            0
        )
    ])

    # Case Solution for Case 1
    cursor.execute("""
    INSERT INTO case_solutions (case_id, culprit_suspect_id, weapon_clue_id, key_proof_clue_id, motive_summary, full_verdict_narrative)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "case_sapphire",
        "suspect_yvonne",
        "clue_wax_impression",
        "clue_train_ticket",
        "Pre-arranged international fence sale to a private European billionaire for €4,000,000.",
        "Madame Yvonne Delacroix used her social access to lift Lord Blackwood's key from his cloak, took a wax mold in the gallery, and returned it unnoticed. At 11:35 PM, she fed the guard dogs raw steak spiked with French valerian sedative, slipped through the West Terrace in the rain, and unlocked the vault. Caught with the lavender wax mold, plum silk threads on the thorns, and a secret 4:30 AM Eurostar ticket to flee the country, Madame Delacroix collapsed in defeat as the Scotland Yard handcuffs clicked shut around her wrists!"
    ))

    # ==========================================
    # CASE 2: The Cyanide Sonata
    # ==========================================
    cursor.execute("""
    INSERT INTO cases (id, title, tagline, difficulty, case_number, location, incident_time, victim, victim_role, briefing, incident_summary, icon, badge_color)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "case_sonata",
        "The Cyanide Sonata",
        "A ruthless maestro collapsed dead at his podium during a stormy dress rehearsal.",
        "Hard",
        "CASE-092-B",
        "The Royal St. Jude Concert Hall, London",
        "8:15 PM, Act II Rehearsal",
        "Maestro Arturo Vane",
        "World-Renowned Orchestra Conductor",
        "During the climactic crescendo of Tchaikovsky's 6th Symphony, tyrannical conductor Arturo Vane clutched his throat, gasped for breath, and collapsed off his podium. Paramedics pronounced him dead on arrival: cyanide poisoning. On his conductor's music stand sat his customary porcelain mug of steaming chamomile honey tea. The stage doors were secured against the storm, trapping all four key members backstage.",
        "The toxicologist confirmed lethal potassium cyanide in the tea mug. The water was boiled in the backstage green room. Only four people had unsupervised access to the maestro's private refreshments prior to the baton downbeat at 8:00 PM.",
        "fa-music",
        "#8b5cf6"
    ))

    # Crime scenes for Case 2
    cursor.executemany("""
    INSERT INTO crime_scenes (id, case_id, name, description, icon)
    VALUES (?, ?, ?, ?, ?)
    """, [
        ("scene_podium", "case_sonata", "The Conductor's Podium", "Center stage. Music stand knocked over, broken baton, and a half-empty porcelain tea mug.", "fa-drum"),
        ("scene_greenroom", "case_sonata", "The Private Green Room", "Vane's luxurious private dressing suite. Kettle, honey jar, tea caddy, and a locked desk.", "fa-couch"),
        ("scene_backstage", "case_sonata", "Stage Left Wing & Prop Room", "Dimmers, cables, instrument cases, soundboard, and lockers for stage hands.", "fa-theater-masks"),
        ("scene_library", "case_sonata", "The Music Archive & Library", "Shelves of bound orchestral scores, manuscript paper, photocopier, and paper shredder.", "fa-archive")
    ])

    # Suspects for Case 2
    cursor.executemany("""
    INSERT INTO suspects (id, case_id, name, role, age, avatar_svg, bio, initial_statement, motive_hint, alibi_claim, is_culprit, confession, innocent_statement)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            "suspect_elena",
            "case_sonata",
            "Elena Rostova",
            "First Violinist & Concertmaster",
            34,
            "violinist",
            "A virtuosic perfectionist who has led the string section for seven seasons. Known for fierce artistic battles with Vane.",
            "I was on stage tuning my Stradivarius with the oboist from 7:45 PM until the Maestro stepped on stage.",
            "Vane had threatened to terminate her contract tomorrow morning and replace her with a protégé.",
            "Claims she sat in Section A tuning her violin in full view of the orchestra.",
            0,
            "",
            "I despised the man's cruelty, Detective, but I am an artist! I was going to ruin him by walking out with the entire violin section before the Royal Gala!"
        ),
        (
            "suspect_oliver",
            "case_sonata",
            "Oliver Finch",
            "Stage Manager",
            48,
            "stage_manager",
            "Runs the theatre backstage with military precision. Personally prepares the Maestro's tea service before every rehearsal.",
            "I prepared the Maestro's chamomile tea at 7:40 PM, carried the tray to his podium at 7:55 PM, and immediately returned to the lighting board.",
            "His daughter was an aspiring soprano who committed suicide after Vane viciously humiliated and blackballed her from the opera.",
            "Claims he never left the stage left lighting console between 7:50 PM and the incident.",
            1,
            "He laughed! Do you know what Arturo Vane said when I begged him to give my sweet Clara another audition three years ago? He told her she had 'the vocal range of a dying toad' and phoned every conservatory in Europe to bury her! She threw herself into the Thames, and he drank vintage champagne! The tea was sweet, wasn't it, Maestro?! May you burn in hell!",
            ""
        ),
        (
            "suspect_clara_b",
            "case_sonata",
            "Clara Bell",
            "Understudy Pianist",
            25,
            "pianist",
            "A brilliant young prodigy whose original piano concerto was stolen and published under Vane's name.",
            "I was in the basement archive practicing my cadenza on the upright piano with headphones.",
            "Discovered yesterday that Vane collected £200,000 in royalties from music she composed.",
            "Claims she was practicing alone in the lower practice cellar from 7:30 to 8:15 PM.",
            0,
            "",
            "I was suing him in the High Court for copyright theft! My lawyers filed the injunction at noon! If he dies, the rights stay tied up in his estate for decades—his death ruins my legal claim!"
        ),
        (
            "suspect_marcus",
            "case_sonata",
            "Marcus Sterling",
            "Philharmonic Chairman & Patron",
            59,
            "patron",
            "A wealthy industrialist funding the orchestra. Secretly bleeding cash from embezzlement.",
            "I was in the private box watching rehearsal with my binoculars and reviewing the season ledger.",
            "Vane uncovered Sterling's embezzlement of the endowment fund and demanded hush money.",
            "Claims he never came downstairs from the VIP Mezzanine box.",
            0,
            "",
            "Vane was blackmailing me for half a million pounds! Do you think I'd poison him with a whole auditorium watching? I was waiting for my offshore wire transfer to clear!"
        )
    ])

    # Clues for Case 2
    cursor.executemany("""
    INSERT INTO clues (id, case_id, scene_id, title, category, short_desc, full_analysis, icon, is_key_evidence)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            "clue_spiked_mug",
            "case_sonata",
            "scene_podium",
            "Cyanide-Laced Porcelain Mug",
            "Forensic",
            "Maestro Vane's personal tea mug with Chamomile tea residue and bitter almond smell.",
            "Toxicology analysis: 400mg of potassium cyanide dissolved inside the remaining liquid. The lethal dose was placed directly into the honey-tea blend.",
            "fa-mug-hot",
            1
        ),
        (
            "clue_honey_dipper",
            "case_sonata",
            "scene_greenroom",
            "The Green Room Honey Jar",
            "Forensic",
            "The jar of Scottish heather honey used exclusively for Vane's drinks.",
            "The honey jar itself is pure and untainted. The cyanide was introduced after the tea was poured, not in the main kettle or honey container.",
            "fa-jar",
            1
        ),
        (
            "clue_photo_locket",
            "case_sonata",
            "scene_backstage",
            "Tarnished Silver Photo Locket",
            "Document",
            "Found beneath the lighting console in Stage Left with a broken hinge.",
            "Contains a photograph of a young soprano girl inscribed: 'To Dad, my biggest fan - Clara'. Tucked inside is a chemist's paper packet labeled 'Potassium Cyanide - Pest Control' with white residue.",
            "fa-portrait",
            1
        ),
        (
            "clue_stage_cue_sheet",
            "case_sonata",
            "scene_backstage",
            "Stage Manager's Duty Log",
            "Document",
            "Oliver Finch's clipboard tracking cues, backstage access, and beverage delivery.",
            "Notates: '7:50 PM - Tea steeped. 7:55 PM - Hand-delivered mug to podium.' Only Finch touched the cup between the kitchen and the podium.",
            "fa-clipboard-list",
            1
        ),
        (
            "clue_violins_scoresheet",
            "case_sonata",
            "scene_podium",
            "Marked Rehearsal Score",
            "Document",
            "The Maestro's score sheets with angry red annotations.",
            "Vicious insults scribbled across the violin parts: 'Elena plays like a butcher. Replace her by Friday.'",
            "fa-file-signature",
            0
        ),
        (
            "clue_embezzlement_audit",
            "case_sonata",
            "scene_library",
            "Confidential Audit Binder",
            "Document",
            "Discovered in the archive safe: proof of £450,000 diverted from the musicians' pension.",
            "Transfers bear Marcus Sterling's signature, with an extortion note from Vane demanding monthly payouts.",
            "fa-money-bill-wave",
            0
        )
    ])

    # Dialogues for Case 2
    cursor.executemany("""
    INSERT INTO suspect_dialogues (suspect_id, topic, question, answer, reaction_mood, unlocks_clue_id)
    VALUES (?, ?, ?, ?, ?, ?)
    """, [
        # Oliver dialogues
        ("suspect_oliver", "Tea Preparation", "Did anyone else touch the Maestro's tea after you brewed it?", "Nobody. The kettle was in the green room. I steeped it for five minutes, brought it directly to his music stand at 7:55 PM. I always do.", "calm", "clue_stage_cue_sheet"),
        ("suspect_oliver", "Family", "Do you have any family ties in the performing arts?", "My... my daughter passed away a few years ago. She was a student. It has nothing to do with this horrific accident.", "nervous", None),
        ("suspect_oliver", "Backstage Chemicals", "Do you keep rat poison or chemicals in the stage workshop?", "Only standard floor cleaners. The exterminators handle pest control, Detective.", "calm", None),

        # Elena dialogues
        ("suspect_elena", "Firing Threat", "Did you know Vane wrote notes planning to replace you by Friday?", "He wrote that every week! Arturo was a megalomaniac. If I wanted him gone, I would play the concert so magnificently the board would fire HIM for failing to keep pace with me!", "angry", None),
        ("suspect_elena", "Stage Presence", "Did you walk near the podium before the downbeat?", "I went to place my tuning fork on the cello riser at 7:52 PM, but I never touched his tea. Elena Rostova does not poison drinks!", "calm", None),

        # Clara Bell dialogues
        ("suspect_clara_b", "The Stolen Concerto", "Vane took credit for your piano concerto, didn't he?", "Yes! He called it 'Symphonic Meditation No. 4'. But my copyright lawsuit was going to be heard in court next Tuesday! His death halts the injunction. Why would I shoot myself in the foot?", "calm", None),

        # Marcus dialogues
        ("suspect_marcus", "Extortion", "Vane was blackmailing you over the pension deficit.", "The Maestro was a vulture! But my financial lawyers were drafting a non-disclosure settlement. Murder solves nothing—it invites police into my books, as you are doing now!", "angry", None)
    ])

    # Contradictions for Case 2
    cursor.executemany("""
    INSERT INTO contradictions (suspect_id, clue_id, callout_text, suspect_response, breaks_alibi)
    VALUES (?, ?, ?, ?, ?)
    """, [
        (
            "suspect_oliver",
            "clue_photo_locket",
            "We found this silver locket under your lighting console containing a photo of your daughter Clara—and a chemist's paper packet with potassium cyanide residue!",
            "My... my daughter's locket... where did you... you don't know the pain I've lived with!",
            1
        ),
        (
            "suspect_oliver",
            "clue_honey_dipper",
            "The green room honey jar and kettle were untainted. The cyanide was added directly into the mug while in transit to the podium—a journey only YOU undertook!",
            "I... someone else could have slipped something into it while my back was turned! It was dark backstage!",
            1
        ),
        (
            "suspect_oliver",
            "clue_stage_cue_sheet",
            "Your own stage log confirms you held custody of the tea right until 7:55 PM, five minutes before Vane took his first sip at the podium downbeat!",
            "He deserved it! He drove her to the river! He deserved every drop!",
            1
        )
    ])

    # Case Solution for Case 2
    cursor.execute("""
    INSERT INTO case_solutions (case_id, culprit_suspect_id, weapon_clue_id, key_proof_clue_id, motive_summary, full_verdict_narrative)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "case_sonata",
        "suspect_oliver",
        "clue_spiked_mug",
        "clue_photo_locket",
        "Revenge for driving his opera-singer daughter Clara to suicide through ruthless career sabotage.",
        "Stage Manager Oliver Finch harbored burning grief for three years after Maestro Vane cruelly ruined his daughter's opera dreams, leading to her suicide. Armed with industrial cyanide obtained from theatre pest stores, Finch steeped the Maestro's tea at 7:50 PM, stirred the lethal poison directly into the porcelain cup with his daughter's locket packet, and placed it on the podium stand. Confronted with the dropped silver locket containing cyanide dust and his sole custody of the beverage, Finch broke down in tears, crying out his daughter's name as officers escorted him away."
    ))

    # ==========================================
    # CASE 3: The Silicon Vault Sabotage
    # ==========================================
    cursor.execute("""
    INSERT INTO cases (id, title, tagline, difficulty, case_number, location, incident_time, victim, victim_role, briefing, incident_summary, icon, badge_color)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "case_cyber",
        "The Silicon Vault Sabotage",
        "A quantum AI architect poisoned inside an airtight, biometric-locked server room.",
        "Expert",
        "CASE-105-C",
        "NeuroCore Quantum Labs, Level -3 Cleanroom, Cambridge",
        "2:15 AM, Server Backup Window",
        "Dr. Aris Thorne",
        "Chief Quantum AI Scientist",
        "At 2:15 AM, alarms sounded in the subterranean cleanroom of NeuroCore Labs. Dr. Aris Thorne was found unconscious and asphyxiated inside the airtight quantum computer vault. The primary optical drive containing 'Project Promethean'—the multi-billion dollar quantum neural core—was physically ripped from the rack and wiped. The vault door has a biometric retina scanner and electromagnetic lock that was never breached from the outside.",
        "Medical autopsy discovered Dr. Thorne died from acute nitrogen gas suffocation. The room's fire suppression system was triggered manually from an emergency terminal. Four personnel were present in the sub-level facility during the 2:00 AM maintenance cycle.",
        "fa-microchip",
        "#10b981"
    ))

    # Crime scenes for Case 3
    cursor.executemany("""
    INSERT INTO crime_scenes (id, case_id, name, description, icon)
    VALUES (?, ?, ?, ?, ?)
    """, [
        ("scene_q_vault", "case_cyber", "The Sub-Zero Quantum Vault", "Chilled to near absolute zero. Racks of quantum processing units, severed optical fiber cables.", "fa-server"),
        ("scene_security_hub", "case_cyber", "Cybersecurity Command Desk", "Monitors displaying biometric access logs, CCTV feeds, and system diagnostics.", "fa-shield-halved"),
        ("scene_airlock", "case_cyber", "Decontamination Airlock", "Hazmat suits, nitrogen scrubbers, sticky mats, and locker bays.", "fa-door-closed"),
        ("scene_lab_office", "case_cyber", "Dr. Thorne's Research Office", "Whiteboards filled with quantum tensor equations, cracked coffee mugs, and encrypted USBs.", "fa-laptop-code")
    ])

    # Suspects for Case 3
    cursor.executemany("""
    INSERT INTO suspects (id, case_id, name, role, age, avatar_svg, bio, initial_statement, motive_hint, alibi_claim, is_culprit, confession, innocent_statement)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            "suspect_sarah",
            "case_cyber",
            "Dr. Sarah Lin",
            "Lead Algorithm Architect",
            32,
            "engineer",
            "Dr. Thorne's second-in-command. Brilliant, intensely ambitious, and recently passed over for promotion.",
            "I was running calibration routines on Terminal 4 in the dry lab from 1:45 AM until the fire sirens screamed.",
            "She discovered Dr. Thorne was planning to open-source the model, rendering her lucrative equity options worthless.",
            "Claims she never entered the airlock corridor between 1:30 AM and the emergency evacuation.",
            0,
            "",
            "I argued with Aris about patent monetization, sure! But I created half that quantum architecture! Destroying the optical core destroyed three years of my life's work!"
        ),
        (
            "suspect_viktor",
            "case_cyber",
            "Viktor Kroll",
            "Head of Physical Security",
            46,
            "security",
            "Ex-military contractor tasked with securing the quantum vault and managing biometric authorization logs.",
            "I was on duty at the primary console watching cameras. The vault door was never opened between 2:00 AM and 2:15 AM.",
            "Deep in debt to an Eastern European corporate syndicate looking to acquire quantum encryption bypass keys.",
            "Claims he was logged in at the main console monitoring external perimeter sensors.",
            1,
            "You don't understand what Thorne was building! Promethean wasn't just another language model—it was capable of breaking 4096-bit RSA banking cryptography in milliseconds! A foreign consortium offered me fifteen million dollars for a cold clone of the optical drive. Thorne walked in during the data dump! I had no choice—I engaged the cleanroom nitrogen purge to kill the alarms and silence him!",
            ""
        ),
        (
            "suspect_maya",
            "case_cyber",
            "Maya Sterling",
            "Systems Firmware Engineer",
            27,
            "sysadmin",
            "Specialist in server cooling and halon fire-suppression infrastructure.",
            "I was replacing coolant pumps in Sector C. The valve replacement took longer than expected due to pipe corrosion.",
            "Has an anonymous whistleblower blog detailing safety violations at NeuroCore.",
            "Claims she was under the subfloor pipes in Sector C with a wrench.",
            0,
            "",
            "I flagged the nitrogen purge override vulnerability two months ago! I wrote three internal tickets warning management that the security console had an unlogged bypass! They ignored me!"
        ),
        (
            "suspect_grant",
            "case_cyber",
            "Harrison Grant",
            "NeuroCore Chief Operating Officer",
            52,
            "ceo",
            "Corporate executive facing a SEC investigation over falsified quantum benchmark test results.",
            "I was in my executive office on Level 1 on a conference call with our Tokyo investors.",
            "Desperate to prevent an external technical audit scheduled for next Monday.",
            "Claims he never came down to Level -3 during the night.",
            0,
            "",
            "If Aris dies and the core is damaged, our stock plunges 80 percent tomorrow morning! Why would I bankrupt my own enterprise?!"
        )
    ])

    # Clues for Case 3
    cursor.executemany("""
    INSERT INTO clues (id, case_id, scene_id, title, category, short_desc, full_analysis, icon, is_key_evidence)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            "clue_nitrogen_purge",
            "case_cyber",
            "scene_q_vault",
            "Manual Nitrogen Override Valve",
            "Forensic",
            "The emergency fire-suppression override was actuated manually, flooding the vault with 100% nitrogen gas.",
            "Fingerprint powder on the physical override valve matches Viktor Kroll's index finger, beneath a layer of thermal grease.",
            "fa-wind",
            1
        ),
        (
            "clue_cloned_keycard",
            "case_cyber",
            "scene_security_hub",
            "RFID Re-writer & Master Firmware Tool",
            "Physical",
            "Found concealed behind the rack ventilation grille in the security command station.",
            "Contains a script designed to spoof the biometric camera feed with a 15-second loop, allowing someone with physical security clearance to enter without generating a log entry.",
            "fa-id-card",
            1
        ),
        (
            "clue_drive_shredder",
            "case_cyber",
            "scene_airlock",
            "High-Field Degausser & Missing Storage Core",
            "Physical",
            "A magnetic degausser wand discovered hidden inside an emergency oxygen canister in the airlock.",
            "The optical drive was extracted, but wiped with the wand after data was cloned onto a military-grade encrypted SSD found stashed in the locker assigned to security staff.",
            "fa-hard-drive",
            1
        ),
        (
            "clue_bank_ledger",
            "case_cyber",
            "scene_security_hub",
            "Encrypted Offshore Transfer Alert",
            "Document",
            "A printout intercepted from the secure terminal printer: €2,500,000 escrow deposit.",
            "Beneficiary account registered in the Cayman Islands tied to Viktor Kroll's personal passport number.",
            "fa-file-invoice-dollar",
            1
        ),
        (
            "clue_algorithm_whiteboard",
            "case_cyber",
            "scene_lab_office",
            "Dr. Thorne's Breakthrough Notes",
            "Document",
            "Whiteboard with mathematical proofs outlining quantum neural optimization.",
            "Shows collaborative notes signed jointly by Thorne and Dr. Sarah Lin, proving mutual academic alignment.",
            "fa-chalkboard-user",
            0
        )
    ])

    # Dialogues for Case 3
    cursor.executemany("""
    INSERT INTO suspect_dialogues (suspect_id, topic, question, answer, reaction_mood, unlocks_clue_id)
    VALUES (?, ?, ?, ?, ?, ?)
    """, [
        ("suspect_viktor", "Access Logs", "Why is there a 15-minute gap in the security camera recording at 2:00 AM?", "The sub-level mainframe was conducting automated backup compression. It always causes minor frame drops.", "calm", "clue_cloned_keycard"),
        ("suspect_viktor", "Nitrogen Valve", "Did you have reason to visit the manual nitrogen valve tonight?", "Negative. The valve is only touched in fire emergencies. I remained seated in front of my monitors.", "nervous", None),
        ("suspect_viktor", "Offshore Finances", "Have you had contact with foreign technology buyers?", "Nonsense. I am a licensed security specialist. My finances are clean.", "angry", "clue_bank_ledger"),

        ("suspect_sarah", "Working Relationship", "Did you resent Dr. Thorne for claiming the patents?", "We had intense debates on open-source philosophy, yes. But Aris was my mentor. I would never harm a hair on his head.", "calm", None),
        ("suspect_maya", "Cooling System", "Could the nitrogen leak have been an accident caused by faulty valves?", "No way. The emergency dump valve requires two simultaneous physical actions: lifting the safety cover and turning the red dial 90 degrees. It was deliberate murder.", "calm", None)
    ])

    # Contradictions for Case 3
    cursor.executemany("""
    INSERT INTO contradictions (suspect_id, clue_id, callout_text, suspect_response, breaks_alibi)
    VALUES (?, ?, ?, ?, ?)
    """, [
        (
            "suspect_viktor",
            "clue_nitrogen_purge",
            "You stated you never touched the emergency valve, yet your latent fingerprint was discovered directly on the manual nitrogen override switch!",
            "I... I might have inspected the valve during my afternoon rounds! That proves nothing!",
            1
        ),
        (
            "suspect_viktor",
            "clue_cloned_keycard",
            "We discovered an RFID firmware re-writer hidden behind your console grille that spoofed the biometric loop to hide your entry into the vault!",
            "Where did you dig that up?! Someone planted that in my desk!",
            1
        ),
        (
            "suspect_viktor",
            "clue_bank_ledger",
            "Your Cayman account received an escrow alert for €2,500,000 from a foreign tech syndicate—matching the stolen quantum core!",
            "Damn it... how did your cyber forensics bypass the encrypted buffer?!",
            1
        )
    ])

    # Case Solution for Case 3
    cursor.execute("""
    INSERT INTO case_solutions (case_id, culprit_suspect_id, weapon_clue_id, key_proof_clue_id, motive_summary, full_verdict_narrative)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "case_cyber",
        "suspect_viktor",
        "clue_nitrogen_purge",
        "clue_drive_shredder",
        "Multi-million euro corporate espionage sale of quantum cryptographic decryption keys.",
        "Head of Security Viktor Kroll abused his security privileges to loop the CCTV surveillance feed and breach the quantum vault to steal the core for an offshore syndicate. Caught red-handed by Dr. Thorne during the data transfer, Kroll engaged the manual nitrogen purge to suffocate the scientist, then wiped the optical drives and hid the clone drive in an oxygen canister. Confronted with his fingerprints on the purge valve, the CCTV loop device, and the offshore bounty escrow, Kroll surrendered to cybercrime authorities."
    ))

    conn.commit()
    conn.close()
    print("Database successfully seeded with 3 full mystery cases!")

if __name__ == "__main__":
    seed()
