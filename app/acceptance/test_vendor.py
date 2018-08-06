from django.test import tag

from test import cases as case

from acceptance.common import generate_schema


@tag('vendor')
class VendorTest(case.AcceptanceTestCase, metaclass = case.MetaAcceptanceSchema):
 
    schema = generate_schema({
        'header': {
            'tags': ('title',),
            'params': {
                'args': '926451519'
            },
            'wait': 'complete',
            'BALL AEROSPACE & TECHNOLOGIES CORPORATION - Discovery': 'title'
        },
        'actions': {
            'unfiltered': {
                'tags': ('all',),
                'params': {'args': '102067378', 'test': 'true'},
                'naics': ('all', 2),
                'membership_filters': (None, 4, 0, 0, {
                    1: ('Mary C. Dickens', '256-964-5213', 'cdickens@colsa.com')
                }, {
                    1: ('VO', 'SDVO')
                }),
                'vendor_sam': ('5/18/19',),
                'vendor_info': ('COLSA CORPORATION', '102067378', '4U825', '965', '$197,000,000'),
                'vendor_address': ('6728 Odyssey Dr', 'Huntsville, AL 35806', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/102067378/csv/?',),
                'contract_table': (5, 'h_date_signed', 'desc', ('Prev', '1'), '2')
            },
            'naics_bmo_1': {
                'tags': ('naics', 'bmo'),
                'params': {'args': '106974876', 'test': 'true', 'naics': '238220'},
                'action': ('#naics-code', 'select[238220]'),
                'naics': ('238220', 15),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Cuong Vu', '610-866-6121', 'cuong.vu@amecfw.com')
                }),
                'vendor_sam': ('1/4/19',),
                'vendor_info': ('AMEC FOSTER WHEELER PROGRAMS, INC.', '106974876', '0FX47', '2,642', '$459,475,040'),
                'vendor_address': ('2475 Northwinds Pkwy Ste 200-260', 'Alpharetta, GA 30009', False),
                'vendor_badges': (),
                'contract_result_info': ('vendor/106974876/csv/?naics=238220',),
                'contract_table': (3, 'h_date_signed', 'desc')
            },
            'naics_bmo_2': {
                'tags': ('naics', 'bmo'),
                'params': {'args': '616858908', 'test': 'true', 'naics': '238220'},
                'action': ('#naics-code', 'select[238220]'),
                'naics': ('238220', 13),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Marc Yates', '270-885-4642 x 165', 'myates@valiantintegrated.com')
                }),
                'vendor_sam': ('7/13/19',),
                'vendor_info': ('ABM GOVERNMENT SERVIVCES, LLC', '616858908', '0UFD5', '100,000', '$4,000,000,000'),
                'vendor_address': ('101 Walton Way', 'Hopkinsville, KY 42240', True),
                'vendor_badges': (),
                'contract_result_info': ('vendor/616858908/csv/?naics=238220',),
                'contract_table': (3, 'h_date_signed', 'desc')
            },
            'naics_bmo_3': {
                'tags': ('naics', 'bmo'),
                'params': {'args': '808649888', 'test': 'true', 'naics': '238290'},
                'action': ('#naics-code', 'select[238290]'),
                'naics': ('238290', 6),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Ian Hada', '202-625-4239', 'Ianh@donohoe.com')
                }),
                'vendor_sam': ('9/18/18',),
                'vendor_info': ('COMPLETE BUILDING SERVICES', '808649888', '4YAL6', '550', '$26'),
                'vendor_address': ('5151 Wisconsin Ave Nw Ste 400', 'Washington, DC 20016', True),
                'vendor_badges': (),
                'contract_result_info': ('vendor/808649888/csv/?naics=238290',),
                'contract_table': (0, 'h_date_signed', 'desc')
            },
            'naics_bmo_4': {
                'tags': ('naics', 'bmo'),
                'params': {'args': '055124077', 'test': 'true', 'naics': '238210'},
                'action': ('#naics-code', 'select[238210]'),
                'naics': ('238210', 15),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Jill Richardson', '270-697-1200', 'jill.richardson@jjwws.com')
                }),
                'vendor_sam': ('4/25/19',),
                'vendor_info': ('J&J WORLDWIDE SERVICES', '055124077', '5P021', '1,470', '$271,300,000'),
                'vendor_address': ('7710 Rialto Blvd Suite 200', 'Austin, TX 78735', True),
                'vendor_badges': (),
                'contract_result_info': ('vendor/055124077/csv/?naics=238210',),
                'contract_table': (1, 'h_date_signed', 'desc')
            },
            'naics_bmo_5': {
                'tags': ('naics', 'bmo'),
                'params': {'args': '847316189', 'test': 'true', 'naics': '561720'},
                'action': ('#naics-code', 'select[561720]'),
                'naics': ('561720', 8),
                'membership_filters': (None, 2, 0, 0, {
                    2: ('Leslie Powers', '770-328-7999', 'lpowers@pmservicescompany.net')
                }),
                'vendor_sam': ('4/11/19',),
                'vendor_info': ('PREVENTIVE MAINTENANCE SERVICE COMPANY', '847316189', '004Q5', '177', '$1,130,000'),
                'vendor_address': ('225 Union Boulevard, Suite 300', 'Lakewood, CO 80228', False),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/847316189/csv/?naics=561720',),
                'contract_table': (0, 'h_date_signed', 'desc')
            },
            'naics_bmo_6': {
                'tags': ('naics', 'bmo'),
                'params': {'args': '039839683', 'test': 'true', 'naics': '561730'},
                'action': ('#naics-code', 'select[561730]'),
                'naics': ('561730', 15),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Patrick Andriuk', '703-677-6401', 'Patrick.andriuk@cbre.com')
                }),
                'vendor_sam': ('2/15/19',),
                'vendor_info': ('CBRE', '039839683', '3G5K7', '29,000', '$5,000,000,000'),
                'vendor_address': ('750 9Th St Nw Ste 900', 'Washington, DC 20001', True),
                'vendor_badges': (),
                'contract_result_info': ('vendor/039839683/csv/?naics=561730',),
                'contract_table': (1, 'h_date_signed', 'desc')
            },
            'naics_bmo_7': {
                'tags': ('naics', 'bmo'),
                'params': {'args': '793374034', 'test': 'true', 'naics': '561621'},
                'action': ('#naics-code', 'select[561621]'),
                'naics': ('561621', 12),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('John Civitelli', '301-596-2440', 'jcivitelli@lbbassociates.com')
                }),
                'vendor_sam': ('2/5/19',),
                'vendor_info': ('LB&B', '793374034', '0V349', '980', '$90,336,000'),
                'vendor_address': ('9891 Brokenland Pkwy Ste 400', 'Columbia, MD 21046', False),
                'vendor_badges': (),
                'contract_result_info': ('vendor/793374034/csv/?naics=561621',),
                'contract_table': (0, 'h_date_signed', 'desc')
            },
            'naics_bmo_8': {
                'tags': ('naics', 'bmo'),
                'params': {'args': '079859134', 'test': 'true', 'naics': '238220'},
                'action': ('#naics-code', 'select[238220]'),
                'naics': ('238220', 12),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Doug Rowles', '678-525-0722', 'doug.rowles@am.jll.com')
                }),
                'vendor_sam': ('8/10/18',),
                'vendor_info': ('JONES, LANG & LASALLE', '079859134', '7EM20', '77,300', '$6,066,366,464'),
                'vendor_address': ('200 E Randolph Dr', 'Chicago, IL 60601', True),
                'vendor_badges': (),
                'contract_result_info': ('vendor/079859134/csv/?naics=238220',),
                'contract_table': (5, 'h_date_signed', 'desc', ('Prev', '1'), '2')
            },
            'naics_bmo_9': {
                'tags': ('naics', 'bmo'),
                'params': {'args': '012722836', 'test': 'true', 'naics': '238160'},
                'action': ('#naics-code', 'select[238160]'),
                'naics': ('238160', 15),
                'membership_filters': (None, 2, 0, 0, {
                    1: ('Eric Harris', '270-874-2233', 'eric.harris@EML1.com'),
                    2: ('Brad Traughber', '270-874-2233', 'Brad.traughber@EML1.com')
                }),
                'vendor_sam': ('6/20/19',),
                'vendor_info': ('EML LLC', '012722836', '1UVM4', '100', '$11,000,000'),
                'vendor_address': ('318 Seaboard Lane Ste 106', 'Franklin, TN 37067', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/012722836/csv/?naics=238160',),
                'contract_table': (2, 'h_date_signed', 'desc')
            },
            'naics_bmo_10': {
                'tags': ('naics', 'bmo'),
                'params': {'args': '039839683', 'test': 'true', 'naics': '531312'},
                'action': ('#naics-code', 'select[531312]'),
                'naics': ('531312', 15),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Patrick Andriuk', '703-677-6401', 'Patrick.andriuk@cbre.com')
                }),
                'vendor_sam': ('2/15/19',),
                'vendor_info': ('CBRE', '039839683', '3G5K7', '29,000', '$5,000,000,000'),
                'vendor_address': ('750 9Th St Nw Ste 900', 'Washington, DC 20001', True),
                'vendor_badges': (),
                'contract_result_info': ('vendor/039839683/csv/?naics=531312',),
                'contract_table': (1, 'h_date_signed', 'desc')
            },
            'naics_bmo_11': {
                'tags': ('naics', 'bmo'),
                'params': {'args': '012722836', 'test': 'true', 'naics': '236220'},
                'action': ('#naics-code', 'select[236220]'),
                'naics': ('236220', 15),
                'membership_filters': (None, 2, 0, 0, {
                    1: ('Eric Harris', '270-874-2233', 'eric.harris@EML1.com'),
                    2: ('Brad Traughber', '270-874-2233', 'Brad.traughber@EML1.com')
                }),
                'vendor_sam': ('6/20/19',),
                'vendor_info': ('EML LLC', '012722836', '1UVM4', '100', '$11,000,000'),
                'vendor_address': ('318 Seaboard Lane Ste 106', 'Franklin, TN 37067', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/012722836/csv/?naics=236220',),
                'contract_table': (3, 'h_date_signed', 'desc')
            },
            'naics_bmo_12': {
                'tags': ('naics', 'bmo'),
                'params': {'args': '106974876', 'test': 'true', 'naics': '541330'},
                'action': ('#naics-code', 'select[541330]'),
                'naics': ('541330', 15),
                'membership_filters': (None, 2, 0, 0, {
                    1: ('Cuong Vu', '610-866-6121', 'cuong.vu@amecfw.com'),
                    2: ('Sheema Hosein', '404-216-0996', 'Sheema.hosein@amecprograms.com')
                }),
                'vendor_sam': ('1/4/19',),
                'vendor_info': ('AMEC FOSTER WHEELER PROGRAMS, INC.', '106974876', '0FX47', '2,642', '$459,475,040'),
                'vendor_address': ('2475 Northwinds Pkwy Ste 200-260', 'Alpharetta, GA 30009', False),
                'vendor_badges': (),
                'contract_result_info': ('vendor/106974876/csv/?naics=541330',),
                'contract_table': (5, 'h_date_signed', 'desc')
            },
            'naics_bmo_13': {
                'tags': ('naics', 'bmo'),
                'params': {'args': '080778868', 'test': 'true', 'naics': '541350'},
                'action': ('#naics-code', 'select[541350]'),
                'naics': ('541350', 10),
                'membership_filters': (None, 2, 0, 0, {
                    2: ('Misty Clardy', '210-231-6060', 'mclardy@native-energy.com')
                }),
                'vendor_sam': ('5/29/19',),
                'vendor_info': ('NATIVE ENERGY & TECHNOLOGY, INC.', '080778868', '1L8Y9', '5', '$2,700,000'),
                'vendor_address': ('12793 Cogburn Ave', 'San Antonio, TX 78249', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/080778868/csv/?naics=541350',),
                'contract_table': (1, 'h_date_signed', 'desc')
            },
            'naics_bmo_14': {
                'tags': ('naics', 'bmo'),
                'params': {'args': '847316189', 'test': 'true', 'naics': '561210'},
                'action': ('#naics-code', 'select[561210]'),
                'naics': ('561210', 8),
                'membership_filters': (None, 2, 0, 0, {
                    2: ('Leslie Powers', '770-328-7999', 'lpowers@pmservicescompany.net')
                }),
                'vendor_sam': ('4/11/19',),
                'vendor_info': ('PREVENTIVE MAINTENANCE SERVICE COMPANY', '847316189', '004Q5', '177', '$1,130,000'),
                'vendor_address': ('225 Union Boulevard, Suite 300', 'Lakewood, CO 80228', False),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/847316189/csv/?naics=561210',),
                'contract_table': (4, 'h_date_signed', 'desc')
            },
            'naics_bmo_15': {
                'tags': ('naics', 'bmo'),
                'params': {'args': '039839683', 'test': 'true', 'naics': '561710'},
                'action': ('#naics-code', 'select[561710]'),
                'naics': ('561710', 15),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Patrick Andriuk', '703-677-6401', 'Patrick.andriuk@cbre.com')
                }),
                'vendor_sam': ('2/15/19',),
                'vendor_info': ('CBRE', '039839683', '3G5K7', '29,000', '$5,000,000,000'),
                'vendor_address': ('750 9Th St Nw Ste 900', 'Washington, DC 20001', True),
                'vendor_badges': (),
                'contract_result_info': ('vendor/039839683/csv/?naics=561710',),
                'contract_table': (1, 'h_date_signed', 'desc')
            },
            'naics_bmo_16': {
                'tags': ('naics', 'bmo'),
                'params': {'args': '793374034', 'test': 'true', 'naics': '562111'},
                'action': ('#naics-code', 'select[562111]'),
                'naics': ('562111', 12),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('John Civitelli', '301-596-2440', 'jcivitelli@lbbassociates.com')
                }),
                'vendor_sam': ('2/5/19',),
                'vendor_info': ('LB&B', '793374034', '0V349', '980', '$90,336,000'),
                'vendor_address': ('9891 Brokenland Pkwy Ste 400', 'Columbia, MD 21046', False),
                'vendor_badges': (),
                'contract_result_info': ('vendor/793374034/csv/?naics=562111',),
                'contract_table': (0, 'h_date_signed', 'desc')
            },
            'naics_bmo_17': {
                'tags': ('naics', 'bmo'),
                'params': {'args': '043203249', 'test': 'true', 'naics': '561730'},
                'action': ('#naics-code', 'select[561730]'),
                'naics': ('561730', 7),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Ervin Caldera', '301-980-2635', 'Ervin.caldera@mcdean.com')
                }),
                'vendor_sam': ('5/21/19',),
                'vendor_info': ('M.C. DEAN, INC.', '043203249', '3K773', '2,844', '$654,905,280'),
                'vendor_address': ('1765 Greensboro Station Place Suite 1400', 'Tysons, VA 22102', True),
                'vendor_badges': (),
                'contract_result_info': ('vendor/043203249/csv/?naics=561730',),
                'contract_table': (0, 'h_date_signed', 'desc')
            },
            'naics_bmo_sb_1': {
                'tags': ('naics', 'bmo_sb'),
                'params': {'args': '129304551', 'test': 'true', 'naics': '238220'},
                'action': ('#naics-code', 'select[238220]'),
                'naics': ('238220', 15),
                'membership_filters': (None, 2, 0, 0, {
                    1: ('Donald Hill III', '202-434-8470', 'dhill@actionfacilities.com')
                }, {
                    1: ('SB', 'SDB', 'WO')
                }),
                'vendor_sam': ('1/2/19',),
                'vendor_info': ('ACTION FACILITIES MANAGEMENT, INC.', '129304551', '3EET9', '182', '$14,600,000'),
                'vendor_address': ('115 Malone Dr', 'Morgantown, WV 26501', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/129304551/csv/?naics=238220',),
                'contract_table': (5, 'h_date_signed', 'desc', ('Prev', '1'), '2')
            },
            'naics_bmo_sb_2': {
                'tags': ('naics', 'bmo_sb'),
                'params': {'args': '078650478', 'test': 'true', 'naics': '238220'},
                'action': ('#naics-code', 'select[238220]'),
                'naics': ('238220', 9),
                'membership_filters': (None, 2, 0, 0, {
                    1: ('Katherine Scott', '907-771-5070', 'Katherine.Scott@Chenega.com')
                }, {
                    1: ('SB', 'SDB', '8(a)')
                }),
                'vendor_sam': ('2/16/19',),
                'vendor_info': ('CHENEGA FACILITY MGMT', '078650478', '6TLQ7', '74', '$5,352,998'),
                'vendor_address': ('5726 W Hausman Rd Ste 100', 'San Antonio, TX 78249', False),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/078650478/csv/?naics=238220',),
                'contract_table': (5, 'h_date_signed', 'desc')
            },
            'naics_bmo_sb_3': {
                'tags': ('naics', 'bmo_sb'),
                'params': {'args': '614155380', 'test': 'true', 'naics': '238290'},
                'action': ('#naics-code', 'select[238290]'),
                'naics': ('238290', 13),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Michael Albritton', '910-215-1909', 'malbritton@gcrinc.net')
                }, {
                    1: ('SB', 'VO', 'SDVO', 'VA VIP')
                }),
                'vendor_sam': ('unknown',),
                'vendor_info': ('GOVERNMENT CONTRACTING RESOURCES INC', '614155380', '', '500', '$43,028,692'),
                'vendor_address': ('', '', False),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/614155380/csv/?naics=238290',),
                'contract_table': (5, 'h_date_signed', 'desc')
            },
            'naics_bmo_sb_4': {
                'tags': ('naics', 'bmo_sb'),
                'params': {'args': '090967704', 'test': 'true', 'naics': '238210'},
                'action': ('#naics-code', 'select[238210]'),
                'naics': ('238210', 9),
                'membership_filters': (None, 3, 0, 0, {
                    1: ('Richard Cooke', '909-625-6900', 'Richard.cooke@acepex.com'),
                    2: ("Henry Rhee\nRichard Cooke", '909-625-6900', "Henry.rhee@acepex.com\nRichard.cooke@acepex.com")
                }, {
                    1: ('SB', 'SDB'),
                    2: ('SB', 'SDB')
                }),
                'vendor_sam': ('8/1/19',),
                'vendor_info': ('ACEPEX MANAGEMENT', '090967704', '1A9K1', '500', '$25,000,000'),
                'vendor_address': ('10643 Mills Ave', 'Montclair, CA 91763', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/090967704/csv/?naics=238210',),
                'contract_table': (0, 'h_date_signed', 'desc')
            },
            'naics_bmo_sb_5': {
                'tags': ('naics', 'bmo_sb'),
                'params': {'args': '141611272', 'test': 'true', 'naics': '561720'},
                'action': ('#naics-code', 'select[561720]'),
                'naics': ('561720', 8),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Charles Bonner', '703-787-8100 x 117', 'charles.bonner@nvecorp.com'),
                }, {
                    1: ('SB', 'SDB', 'WO')
                }),
                'vendor_sam': ('3/30/19',),
                'vendor_info': ('NVE INC', '141611272', '3RKV2', '120', '$10,823,413'),
                'vendor_address': ('455 Springpark Place, Suite 200B', 'Herndon, VA 20170', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/141611272/csv/?naics=561720',),
                'contract_table': (5, 'h_date_signed', 'desc', ('Prev', '1'), '2')
            },
            'naics_bmo_sb_6': {
                'tags': ('naics', 'bmo_sb'),
                'params': {'args': '129304551', 'test': 'true', 'naics': '561730'},
                'action': ('#naics-code', 'select[561730]'),
                'naics': ('561730', 15),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Donald Hill III', '202-434-8470', 'dhill@actionfacilities.com'),
                }, {
                    1: ('SB', 'SDB', 'WO')
                }),
                'vendor_sam': ('1/2/19',),
                'vendor_info': ('ACTION FACILITIES MANAGEMENT, INC.', '129304551', '3EET9', '182', '$14,600,000'),
                'vendor_address': ('115 Malone Dr', 'Morgantown, WV 26501', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/129304551/csv/?naics=561730',),
                'contract_table': (1, 'h_date_signed', 'desc')
            },
            'naics_bmo_sb_7': {
                'tags': ('naics', 'bmo_sb'),
                'params': {'args': '052648261', 'test': 'true', 'naics': '561621'},
                'action': ('#naics-code', 'select[561621]'),
                'naics': ('561621', 4),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Weedon Gallagher', '410-379-0080', 'wgallagher@ctsi-fm.com'),
                }, {
                    1: ('SB', 'VO', 'SDVO', 'VA VIP')
                }),
                'vendor_sam': ('6/8/19',),
                'vendor_info': ('CTSI', '052648261', '6JSM3', '17', '$2,800,000'),
                'vendor_address': ('7226 Lee Deforest Dr Ste 105', 'Columbia, MD 21046', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/052648261/csv/?naics=561621',),
                'contract_table': (0, 'h_date_signed', 'desc')
            },
            'naics_bmo_sb_8': {
                'tags': ('naics', 'bmo_sb'),
                'params': {'args': '610940632', 'test': 'true', 'naics': '238220'},
                'action': ('#naics-code', 'select[238220]'),
                'naics': ('238220', 4),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Burnie Peters', '703-963-5476', 'burnie@b3enterprisesllc.com'),
                }, {
                    1: ('SB', 'SDB', 'VO', 'SDVO', 'VA VIP')
                }),
                'vendor_sam': ('1/24/19',),
                'vendor_info': ('B3 ENTERPRISES LLC', '610940632', '47U96', '30', '$14,000,000'),
                'vendor_address': ('11799 Antietam Rd', 'Woodbridge, VA 22192', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/610940632/csv/?naics=238220',),
                'contract_table': (4, 'h_date_signed', 'desc')
            },
            'naics_bmo_sb_9': {
                'tags': ('naics', 'bmo_sb'),
                'params': {'args': '884999491', 'test': 'true', 'naics': '238160'},
                'action': ('#naics-code', 'select[238160]'),
                'naics': ('238160', 5),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Jill Workman', '931-552-7044', 'jworkman@facsvcs.com'),
                }, {
                    1: ('SB', 'WO')
                }),
                'vendor_sam': ('1/2/19',),
                'vendor_info': ('FACILITY SERVICES MANAGEMENT', '884999491', '05HC6', '175', '$9,000,000'),
                'vendor_address': ('1031 Progress Dr', 'Clarksville, TN 37040', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/884999491/csv/?naics=238160',),
                'contract_table': (3, 'h_date_signed', 'desc')
            },
            'naics_bmo_sb_10': {
                'tags': ('naics', 'bmo_sb'),
                'params': {'args': '790993252', 'test': 'true', 'naics': '531312'},
                'action': ('#naics-code', 'select[531312]'),
                'naics': ('531312', 5),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Charles Quinlan', '480-245-6730', 'Chuck.quinlan@koyitlotsina.com'),
                }, {
                    1: ('SB', 'SDB', '8(a)')
                }),
                'vendor_sam': ('4/26/19',),
                'vendor_info': ('KCORP SUPPORT SERVICES INC.', '790993252', '52TJ5', '164', '$8,254,406'),
                'vendor_address': ('1603 College Rd', 'Fairbanks, AK 99709', False),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/790993252/csv/?naics=531312',),
                'contract_table': (0, 'h_date_signed', 'desc')
            },
            'naics_bmo_sb_11': {
                'tags': ('naics', 'bmo_sb'),
                'params': {'args': '080778868', 'test': 'true', 'naics': '236220'},
                'action': ('#naics-code', 'select[236220]'),
                'naics': ('236220', 10),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Misty Clardy', '210-231-6060', 'mclardy@native-energy.com'),
                }, {
                    1: ('SB', 'SDB')
                }),
                'vendor_sam': ('5/29/19',),
                'vendor_info': ('NATIVE ENERGY & TECHNOLOGY, INC.', '080778868', '1L8Y9', '5', '$2,700,000'),
                'vendor_address': ('12793 Cogburn Ave', 'San Antonio, TX 78249', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/080778868/csv/?naics=236220',),
                'contract_table': (3, 'h_date_signed', 'desc')
            },
            'naics_bmo_sb_12': {
                'tags': ('naics', 'bmo_sb'),
                'params': {'args': '064860299', 'test': 'true', 'naics': '541330'},
                'action': ('#naics-code', 'select[541330]'),
                'naics': ('541330', 8),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Sean Gallagher', '301-606-1201', 'sean.gallagher@ravenservices.us'),
                }, {
                    1: ('SB',)
                }),
                'vendor_sam': ('11/27/18',),
                'vendor_info': ('RAVEN SERVICE CORPORATION', '064860299', '1FAN6', '110', '$8,702,394'),
                'vendor_address': ('9200 Church St Ste 203', 'Manassas, VA 20110', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/064860299/csv/?naics=541330',),
                'contract_table': (1, 'h_date_signed', 'desc')
            },
            'naics_bmo_sb_13': {
                'tags': ('naics', 'bmo_sb'),
                'params': {'args': '080778868', 'test': 'true', 'naics': '541350'},
                'action': ('#naics-code', 'select[541350]'),
                'naics': ('541350', 10),
                'membership_filters': (None, 2, 0, 0, {
                    1: ('Misty Clardy', '210-231-6060', 'mclardy@native-energy.com'),
                }, {
                    1: ('SB',)
                }),
                'vendor_sam': ('5/29/19',),
                'vendor_info': ('NATIVE ENERGY & TECHNOLOGY, INC.', '080778868', '1L8Y9', '5', '$2,700,000'),
                'vendor_address': ('12793 Cogburn Ave', 'San Antonio, TX 78249', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/080778868/csv/?naics=541350',),
                'contract_table': (1, 'h_date_signed', 'desc')
            },
            'naics_bmo_sb_14': {
                'tags': ('naics', 'bmo_sb'),
                'params': {'args': '053117149', 'test': 'true', 'naics': '561210'},
                'action': ('#naics-code', 'select[561210]'),
                'naics': ('561210', 15),
                'membership_filters': (None, 2, 0, 0, {
                    1: ("Jonathan Tate", "903-780-0703", "jonathan.tate@rosemarkonline.com"),
                    2: ("Jerry Tate\nJonathan Tate", "903-597-8040\n903-780-0703", "jerry.tate@rosemarkonline.com\njonathan.tate@rosemarkonline.com"),
                }, {
                    1: ('SB',),
                    2: ('SB',)
                }),
                'vendor_sam': ('4/6/19',),
                'vendor_info': ('BEN FITZGERALD REAL ESTATE', '053117149', '1TG18', '100', '$8,679,181'),
                'vendor_address': ('1530 S Southwest Loop 323 Ste 106', 'Tyler, TX 75701', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/053117149/csv/?naics=561210',),
                'contract_table': (5, 'h_date_signed', 'desc', ('Prev', '1'), '2')
            },
            'naics_bmo_sb_15': {
                'tags': ('naics', 'bmo_sb'),
                'params': {'args': '129304551', 'test': 'true', 'naics': '561710'},
                'action': ('#naics-code', 'select[561710]'),
                'naics': ('561710', 15),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Donald Hill III', '202-434-8470', 'dhill@actionfacilities.com'),
                }, {
                    1: ('SB', 'SDB', 'WO')
                }),
                'vendor_sam': ('1/2/19',),
                'vendor_info': ('ACTION FACILITIES MANAGEMENT, INC.', '129304551', '3EET9', '182', '$14,600,000'),
                'vendor_address': ('115 Malone Dr', 'Morgantown, WV 26501', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/129304551/csv/?naics=561710',),
                'contract_table': (1, 'h_date_signed', 'desc')
            },
            'naics_bmo_sb_16': {
                'tags': ('naics', 'bmo_sb'),
                'params': {'args': '079515381', 'test': 'true', 'naics': '562111'},
                'action': ('#naics-code', 'select[562111]'),
                'naics': ('562111', 8),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Josh Wilkerson', '334-872-2228 x 101', 'Josh@SDACFacilityServices.com'),
                }, {
                    1: ('SB', 'SDB', 'VO', 'SDVO')
                }),
                'vendor_sam': ('9/21/18',),
                'vendor_info': ('SDAC FACILITY SERVICE LLC', '079515381', '77M00', '1', '$1'),
                'vendor_address': ('14510 Sw 284Th St', 'Homestead, FL 33033', False),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/079515381/csv/?naics=562111',),
                'contract_table': (0, 'h_date_signed', 'desc')
            },
            'naics_bmo_sb_17': {
                'tags': ('naics', 'bmo_sb'),
                'params': {'args': '053117149', 'test': 'true', 'naics': '561730'},
                'action': ('#naics-code', 'select[561730]'),
                'naics': ('561730', 15),
                'membership_filters': (None, 1, 0, 0, {
                    1: ("Jerry Tate\nJonathan Tate", "903-597-8040\n903-780-0703", "jerry.tate@rosemarkonline.com\njonathan.tate@rosemarkonline.com"),
                }, {
                    1: ('SB',)
                }),
                'vendor_sam': ('4/6/19',),
                'vendor_info': ('BEN FITZGERALD REAL ESTATE', '053117149', '1TG18', '100', '$8,679,181'),
                'vendor_address': ('1530 S Southwest Loop 323 Ste 106', 'Tyler, TX 75701', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/053117149/csv/?naics=561730',),
                'contract_table': (0, 'h_date_signed', 'desc')
            },
            'naics_hcats_1': {
                'tags': ('naics', 'hcats'),
                'params': {'args': '006928857', 'test': 'true', 'naics': '611430'},
                'action': ('#naics-code', 'select[611430]'),
                'naics': ('611430', 33),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Moses Moussessian', '703-984-0305', "moussessian_moses@bah.com\nHCaTS@bah.com"),
                }),
                'vendor_sam': ('7/26/19',),
                'vendor_info': ('BOOZ ALLEN HAMILTON', '006928857', '17038', 'N/A', 'N/A'),
                'vendor_address': ('8283 Greensboro Dr', 'Mclean, VA 22102', True),
                'vendor_badges': (),
                'contract_result_info': ('vendor/006928857/csv/?naics=611430',),
                'contract_table': (5, 'h_date_signed', 'desc', ('Prev', '1'), '2')
            },
            'naics_hcats_2': {
                'tags': ('naics', 'hcats'),
                'params': {'args': '830333824', 'test': 'true', 'naics': '541612'},
                'action': ('#naics-code', 'select[541612]'),
                'naics': ('541612', 9),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Scott L. Green', '301-633-7782', "slgreen@afsc.com\nbids@afsc.com"),
                }),
                'vendor_sam': ('1/11/19',),
                'vendor_info': ('ARMED FORCES SERVICES CORPORATION (AFSC)', '830333824', '1Q8F1', '246', '$24,422,824'),
                'vendor_address': ('2800 S Shirlington Rd Ste 350', 'Arlington, VA 22206', True),
                'vendor_badges': (),
                'contract_result_info': ('vendor/830333824/csv/?naics=541612',),
                'contract_table': (5, 'h_date_signed', 'desc', ('Prev', '1'), '2')
            },
            'naics_hcats_sb_1': {
                'tags': ('naics', 'hcats_sb'),
                'params': {'args': '837788223', 'test': 'true', 'naics': '611430'},
                'action': ('#naics-code', 'select[611430]'),
                'naics': ('611430', 4),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Lisa Sergent', '606-780-0196', "lsergent@powertrain.com\nsbhcats@powertrain.com")
                }, {
                    1: ('WO',)
                }),
                'vendor_sam': ('4/26/19',),
                'vendor_info': ('POWERTRAIN, INC.', '837788223', '1ZLY7', '35', '$7,986,480'),
                'vendor_address': ('8201 Corporate Dr Ste 580', 'Landover, MD 20785', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/837788223/csv/?naics=611430',),
                'contract_table': (5, 'h_date_signed', 'desc', ('Prev', '1'), '2')
            },
            'naics_hcats_sb_2': {
                'tags': ('naics', 'hcats_sb'),
                'params': {'args': '827620308', 'test': 'true', 'naics': '541618'},
                'action': ('#naics-code', 'select[541618]'),
                'naics': ('541618', 6),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Brandon Bloodworth', '202-302-0217', "brandon.bloodworth@barbaricum.com\nHCaTS@barbaricum.com")
                }, {
                    1: ('HubZ', 'VO', 'SDVO')
                }),
                'vendor_sam': ('6/4/19',),
                'vendor_info': ('BARBARICUM', '827620308', '55EW9', '96', '$19,262,048'),
                'vendor_address': ('1714 N Street', 'Washington, DC 20036', False),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/827620308/csv/?naics=541618',),
                'contract_table': (2, 'h_date_signed', 'desc')
            },        
            'naics_oasis_1': {
                'tags': ('naics', 'oasis'),
                'params': {'args': '963450866', 'test': 'true', 'naics': '541380'},
                'action': ('#naics-code', 'select[541380]'),
                'naics': ('541380', 24),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Janet V. LaFever', '703-259-5008', 'OASIS-PMO@alionscience.com')
                }),
                'vendor_sam': ('0/27/19',),
                'vendor_info': ('ALION SCIENCE AND TECHNOLOGY CORPORATION', '963450866', '3BM47', '2,728', '$877,013,440'),
                'vendor_address': ('1000 Burr Ridge Pkwy Ste 202', 'Burr Ridge, IL 60527', False),
                'vendor_badges': (),
                'contract_result_info': ('vendor/963450866/csv/?naics=541380',),
                'contract_table': (5, 'h_date_signed', 'desc')
            },
            'naics_oasis_2': {
                'tags': ('naics', 'oasis'),
                'params': {'args': '139727148', 'test': 'true', 'naics': '541214'},
                'action': ('#naics-code', 'select[541214]'),
                'naics': ('541214', 43),
                'membership_filters': (None, 2, 0, 0, {
                    1: ('Tania Koles', '571-414-4033', 'OASIS@accenturefederal.com')
                }),
                'vendor_sam': ('4/5/19',),
                'vendor_info': ('ACCENTURE FEDERAL SERVICES LLC', '139727148', '1ZD18', '380', '$65,000,000'),
                'vendor_address': ('800 North Glebe Rd #300', 'Arlington, VA 22203', True),
                'vendor_badges': (),
                'contract_result_info': ('vendor/139727148/csv/?naics=541214',),
                'contract_table': (0, 'h_date_signed', 'desc')
            },
            'naics_oasis_3': {
                'tags': ('naics', 'oasis'),
                'params': {'args': '926451519', 'test': 'true', 'naics': '541330'},
                'action': ('#naics-code', 'select[541330]'),
                'naics': ('541330', 24),
                'membership_filters': (None, 2, 0, 0, {
                    2: ('Gayle Ashton', '937-320-7054', 'gashton@ball.com')
                }),
                'vendor_sam': ('2/9/19',),
                'vendor_info': ('BALL AEROSPACE & TECHNOLOGIES CORPORATION', '926451519', '13993', '2,800', '$850,000,000'),
                'vendor_address': ('1600 Commerce St', 'Boulder, CO 80301', True),
                'vendor_badges': (),
                'contract_result_info': ('vendor/926451519/csv/?naics=541330',),
                'contract_table': (5, 'h_date_signed', 'desc')
            },
            'naics_oasis_4': {
                'tags': ('naics', 'oasis'),
                'params': {'args': '097967608', 'test': 'true', 'naics': '541712'},
                'action': ('#naics-code', 'select[541712]'),
                'naics': ('541712', 24),
                'membership_filters': (None, 5, 0, 5, {
                    2: ('Michelle P. Eckstein', '505-881-8074', 'ARA_OASIS_SB@ara.com')
                }),
                'vendor_sam': ('1/10/19',),
                'vendor_info': ('APPLIED RESEARCH ASSOCIATES, INC., DBA ARA', '097967608', '9R446', '1,072', '$223,746,560'),
                'vendor_address': ('4300 San Mateo Blvd Ne Ste A-220', 'Albuquerque, NM 87110', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/097967608/csv/?naics=541712',),
                'contract_table': (0, 'h_date_signed', 'desc')
            },
            'naics_oasis_5a': {
                'tags': ('naics', 'oasis'),
                'params': {'args': '007901598', 'test': 'true', 'naics': '541712'},
                'action': ('#naics-code', 'select[541712]'),
                'naics': ('541712', 29),
                'membership_filters': (None, 4, 0, 0, {
                    2: ('Lee Donelson', '410-306-8554', 'OASIS@battelle.org')
                }),
                'vendor_sam': ('2/27/19',),
                'vendor_info': ('BATTELLE MEMORIAL INSTITUTE', '007901598', '79986', '20,000', '$5,174,514,176'),
                'vendor_address': ('505 King Avenue', 'Columbus, OH 43201', True),
                'vendor_badges': (),
                'contract_result_info': ('vendor/007901598/csv/?naics=541712',),
                'contract_table': (3, 'h_date_signed', 'desc')
            },
            'naics_oasis_5b': {
                'tags': ('naics', 'oasis'),
                'params': {'args': '097967608', 'test': 'true', 'naics': '541712'},
                'action': ('#naics-code', 'select[541712]'),
                'naics': ('541712', 24),
                'membership_filters': (None, 5, 0, 5, {
                    2: ('Michelle P. Eckstein', '505-881-8074', 'ARA_OASIS_SB@ara.com')
                }),
                'vendor_sam': ('1/10/19',),
                'vendor_info': ('APPLIED RESEARCH ASSOCIATES, INC., DBA ARA', '097967608', '9R446', '1,072', '$223,746,560'),
                'vendor_address': ('4300 San Mateo Blvd Ne Ste A-220', 'Albuquerque, NM 87110', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/097967608/csv/?naics=541712',),
                'contract_table': (0, 'h_date_signed', 'desc')
            },
            'naics_oasis_6': {
                'tags': ('naics', 'oasis'),
                'params': {'args': '075458455', 'test': 'true', 'naics': '541712'},
                'action': ('#naics-code', 'select[541712]'),
                'naics': ('541712', 2),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Rosie Maul', '256-964-4567', 'OASIS@dynetics.com')
                }),
                'vendor_sam': ('4/24/19',),
                'vendor_info': ('DYNETICS, INC.', '075458455', '7L855', '1,380', '$216,551,872'),
                'vendor_address': ('1002 Explorer Blvd', 'Huntsville, AL 35806', True),
                'vendor_badges': (),
                'contract_result_info': ('vendor/075458455/csv/?naics=541712',),
                'contract_table': (1, 'h_date_signed', 'desc')
            },
            'naics_oasis_sb_1': {
                'tags': ('naics', 'oasis_sb'),
                'params': {'args': '170203199', 'test': 'true', 'naics': '541612'},
                'action': ('#naics-code', 'select[541612]'),
                'naics': ('541612', 22),
                'membership_filters': (None, 1, 0, 1, {
                    1: ('Denise Penn', '719-418-4968', 'OASISPOOL1@apogeemail.net')
                }, {
                    1: ('8(a)',)
                }),
                'vendor_sam': ('3/11/19',),
                'vendor_info': ('APOGEE ENGINEERING, LLC', '170203199', '35CZ6', '62', '$5,686,000'),
                'vendor_address': ('8610 Explorer Dr Ste 305', 'Colorado Springs, CO 80920', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/170203199/csv/?naics=541612',),
                'contract_table': (5, 'h_date_signed', 'desc', ('Prev', '1'), '2')
            },
            'naics_oasis_sb_2': {
                'tags': ('naics', 'oasis_sb'),
                'params': {'args': '825487130', 'test': 'true', 'naics': '541214'},
                'action': ('#naics-code', 'select[541214]'),
                'naics': ('541214', 6),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('Nazim Hamilton', '202-204-2238', 'Nazim.Hamilton@usfti.com')
                }, {
                    1: ('8(a)',)
                }),
                'vendor_sam': ('11/21/18',),
                'vendor_info': ('HAMILTON ENTERPRISES, LLC DBA FRANKLIN AND TURNER INTERNATIONAL', '825487130', '52DB6', '15', '$2,500,000'),
                'vendor_address': ('7327 Hanover Parkway, Suite A', 'Greenbelt, MD 20770', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/825487130/csv/?naics=541214',),
                'contract_table': (5, 'h_date_signed', 'desc', ('Prev', '1'), '2')
            },
            'naics_oasis_sb_3': {
                'tags': ('naics', 'oasis_sb'),
                'params': {'args': '039872622', 'test': 'true', 'naics': '541330'},
                'action': ('#naics-code', 'select[541330]'),
                'naics': ('541330', 7),
                'membership_filters': (None, 1, 0, 1, {
                    1: ('Lynna S. Hood', '571-257-4785', 'lhood@addxcorp.com')
                }, {
                    1: ('SB', 'VO', 'SDVO')
                }),
                'vendor_sam': ('10/16/18',),
                'vendor_info': ('ADDX CORPORATION', '039872622', '1XPA3', '62', '$16,534,185'),
                'vendor_address': ('4900 Seminary Rd Ste 700', 'Alexandria, VA 22311', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/039872622/csv/?naics=541330',),
                'contract_table': (5, 'h_date_signed', 'desc', ('Prev', '1'), '2')
            },
            'naics_oasis_sb_4': {
                'tags': ('naics', 'oasis_sb'),
                'params': {'args': '124651964', 'test': 'true', 'naics': '541711'},
                'action': ('#naics-code', 'select[541711]'),
                'naics': ('541711', 3),
                'membership_filters': (None, 1, 0, 1, {
                    1: ('Kelly L Bain', '719-475-0605 x 1001', 'kbain@deltasands.com')
                }, {
                    1: ('VO', 'SDVO')
                }),
                'vendor_sam': ('2/23/19',),
                'vendor_info': ('DELTA SOLUTIONS & STRATEGIES, LLC', '124651964', '1RUU6', '75', '$12,600,000'),
                'vendor_address': ('7150 Campus Drive, Suite 365', 'Colorado Springs, CO 80920', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/124651964/csv/?naics=541711',),
                'contract_table': (3, 'h_date_signed', 'desc')
            },
            'naics_oasis_sb_5a': {
                'tags': ('naics', 'oasis_sb'),
                'params': {'args': '968706106', 'test': 'true', 'naics': '541712'},
                'action': ('#naics-code', 'select[541712]'),
                'naics': ('541712', 24),
                'membership_filters': (None, 3, 0, 0, {
                    2: ('Benjamin W. Saunders', '571-266-2986', 'OASIS@asrcfederal.com')
                }, {
                    2: ('8(a)',)
                }),
                'vendor_sam': ('2/26/19',),
                'vendor_info': ('ARCTIC SLOPE TECHNICAL SERVICES, INC.', '968706106', '6HBK6', '445', '$48,021,632'),
                'vendor_address': ('7000 Muirkirk Meadows Dr', 'Beltsville, MD 20705', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/968706106/csv/?naics=541712',),
                'contract_table': (5, 'h_date_signed', 'desc', ('Prev', '1'), '2')
            },
            'naics_oasis_sb_5b': {
                'tags': ('naics', 'oasis_sb'),
                'params': {'args': '807990382', 'test': 'true', 'naics': '541712'},
                'action': ('#naics-code', 'select[541712]'),
                'naics': ('541712', 2),
                'membership_filters': (None, 3, 0, 3, {
                    2: ('Bryce Skinn', '937-912-6115', 'bskinn@appliedres.com')
                }),
                'vendor_sam': ('3/8/19',),
                'vendor_info': ('APPLIED RESEARCH SOLUTIONS, INC.', '807990382', '4YHD4', '580', '$110,000,000'),
                'vendor_address': ('51 Plum St Ste 240', 'Beavercreek, OH 45440', False),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/807990382/csv/?naics=541712',),
                'contract_table': (5, 'h_date_signed', 'desc', ('Prev', '1'), '2')
            },
            'naics_oasis_sb_6': {
                'tags': ('naics', 'oasis_sb'),
                'params': {'args': '883504854', 'test': 'true', 'naics': '541712'},
                'action': ('#naics-code', 'select[541712]'),
                'naics': ('541712', 3),
                'membership_filters': (None, 3, 0, 3, {
                    3: ('Ronald Vance', '937-431-9431 x 5899', 'BTASGSAOASIS@btas.com')
                }, {
                    3: ('WO',)
                }),
                'vendor_sam': ('7/10/19',),
                'vendor_info': ('BTAS, INC. DBA BUSINESS TECHNOLOGIES & SOLUTIONS', '883504854', '07GB6', '225', '$16,884,040'),
                'vendor_address': ('4391 Dayton-Xenia Rd', 'Beavercreek, OH 45432', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/883504854/csv/?naics=541712',),
                'contract_table': (4, 'h_date_signed', 'desc')
            },
            'naics_pss_382': {
                'tags': ('naics', 'pss'),
                'params': {'args': '962857244', 'test': 'true', 'naics': '541930'},
                'action': ('#naics-code', 'select[541930]'),
                'naics': ('541930', 2),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('', '301-408-4242', 'lena@ad-astrainc.com'),
                }, {
                    1: ('SB', 'SDB', 'WO')
                }),
                'vendor_sam': ('2/15/19',),
                'vendor_info': ('AD ASTRA INC.', '962857244', '61VV7', '9', '$3,800,000'),
                'vendor_address': ('8701 Georgia Ave Ste 800', 'Silver Spring, MD 20910', False),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/962857244/csv/?naics=541930',),
                'contract_table': (5, 'h_date_signed', 'desc', ('Prev', '1'), '2')
            },
            'naics_pss_520': {
                'tags': ('naics', 'pss'),
                'params': {'args': '621297568', 'test': 'true', 'naics': '541611'},
                'action': ('#naics-code', 'select[541611]'),
                'naics': ('541611', 13),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('', '202-498-5388', 'aclarke@accurateconceptions.com'),
                }, {
                    1: ('SB', 'SDB', '8(a)', 'HubZ')
                }),
                'vendor_sam': ('4/16/19',),
                'vendor_info': ('ACCURATE CONCEPTIONS, L.L.C.', '621297568', '4BQH5', '9', '$1,200,000'),
                'vendor_address': ('19 O St Sw', 'Washington, DC 20024', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/621297568/csv/?naics=541611',),
                'contract_table': (5, 'h_date_signed', 'desc', ('Prev', '1'), '2')
            },
            'naics_pss_541': {
                'tags': ('naics', 'pss'),
                'params': {'args': '013781294', 'test': 'true', 'naics': '541613'},
                'action': ('#naics-code', 'select[541613]'),
                'naics': ('541613', 11),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('', '202-962-3955', 'SHERRY.LUPISELLA@720STRATEGIES.COM'),
                }, {
                    1: ('SB',)
                }),
                'vendor_sam': ('6/4/19',),
                'vendor_info': ('720 STRATEGIES, LLC', '013781294', '67PL3', '25', '$7,127,114'),
                'vendor_address': ('1220 19Th St Nw Ste 300', 'Washington, DC 20036', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/013781294/csv/?naics=541613',),
                'contract_table': (0, 'h_date_signed', 'desc')
            },
            'naics_pss_871': {
                'tags': ('naics', 'pss'),
                'params': {'args': '828985940', 'test': 'true', 'naics': '236220'},
                'action': ('#naics-code', 'select[236220]'),
                'naics': ('236220', 5),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('', '732-493-1700', 'nmanheimer@aaski.com'),
                }),
                'vendor_sam': ('2/1/19',),
                'vendor_info': ('AASKI TECHNOLOGY INC', '828985940', '59JH6', '417', '$241,837,216'),
                'vendor_address': ('1104 S Philadelphia Blvd #800', 'Aberdeen, MD 21001', True),
                'vendor_badges': (),
                'contract_result_info': ('vendor/828985940/csv/?naics=236220',),
                'contract_table': (3, 'h_date_signed', 'desc')
            },
            'naics_pss_874': {
                'tags': ('naics', 'pss'),
                'params': {'args': '114214211', 'test': 'true', 'naics': '541611'},
                'action': ('#naics-code', 'select[541611]'),
                'naics': ('541611', 16),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('', '703-840-3491', 'doc.grantham@6Ksystems.com'),
                }, {
                    1: ('SDB', '8(a)')
                }),
                'vendor_sam': ('6/28/19',),
                'vendor_info': ('6K SYSTEMS, INC.', '114214211', '1ZJK7', '100', '$5,666,666'),
                'vendor_address': ('11710 Plaza America Dr Ste 810', 'Reston, VA 20190', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/114214211/csv/?naics=541611',),
                'contract_table': (5, 'h_date_signed', 'desc', ('Prev', '1'), '2')
            },
            'naics_pss_874500': {
                'tags': ('naics', 'pss'),
                'params': {'args': '080117787', 'test': 'true', 'naics': '238220'},
                'action': ('#naics-code', 'select[238220]'),
                'naics': ('238220', 11),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('', '478-923-9041', 'ddomingue@advanced-core.com'),
                }, {
                    1: ('SDB', '8(a)')
                }),
                'vendor_sam': ('7/5/19',),
                'vendor_info': ('ADVANCED CORE CONCEPTS, LLC', '080117787', '7JRY5', '30', '$4,900,000'),
                'vendor_address': ('645 Tallulah Trl Ste 201', 'Warner Robins, GA 31088', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/080117787/csv/?naics=238220',),
                'contract_table': (1, 'h_date_signed', 'desc')
            },
            'naics_pss_899': {
                'tags': ('naics', 'pss'),
                'params': {'args': '038523239', 'test': 'true', 'naics': '541620'},
                'action': ('#naics-code', 'select[541620]'),
                'naics': ('541620', 7),
                'membership_filters': (None, 1, 0, 0, {
                    1: ('', '907-455-6777', 'tdelong@abrinc.com'),
                }, {
                    1: ('SB',)
                }),
                'vendor_sam': ('11/20/18',),
                'vendor_info': ('ABR INC', '038523239', '0Y330', '49', '$13,967,623'),
                'vendor_address': ('2842 Goldstream Rd', 'Fairbanks, AK 99709', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/038523239/csv/?naics=541620',),
                'contract_table': (5, 'h_date_signed', 'desc', ('Prev', '1'), '2')
            },     
            'membership_pss_382': {
                'tags': ('membership', 'pss'),
                'params': {'args': '962857244', 'test': 'true', 'memberships': 'GS10F177AA'},
                'action': ('#GS10F177AA', 'click'),
                'naics': ('all', 2),
                'membership_filters': (None, 1, 1, 0, {
                    1: ('', '301-408-4242', 'lena@ad-astrainc.com'),
                }, {
                    1: ('SB', 'SDB', 'WO')
                }),
                'vendor_sam': ('2/15/19',),
                'vendor_info': ('AD ASTRA INC.', '962857244', '61VV7', '9', '$3,800,000'),
                'vendor_address': ('8701 Georgia Ave Ste 800', 'Silver Spring, MD 20910', False),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/962857244/csv/?memberships=GS10F177AA',),
                'contract_table': (3, 'h_date_signed', 'desc')
            },
            'membership_pss_520': {
                'tags': ('membership', 'pss'),
                'params': {'args': '621297568', 'test': 'true', 'memberships': 'GS23F006AA'},
                'action': ('#GS23F006AA', 'click'),
                'naics': ('all', 13),
                'membership_filters': (None, 1, 1, 0, {
                    1: ('', '202-498-5388', 'aclarke@accurateconceptions.com'),
                }, {
                    1: ('SB', 'SDB', '8(a)', 'HubZ')
                }),
                'vendor_sam': ('4/16/19',),
                'vendor_info': ('ACCURATE CONCEPTIONS, L.L.C.', '621297568', '4BQH5', '9', '$1,200,000'),
                'vendor_address': ('19 O St Sw', 'Washington, DC 20024', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/621297568/csv/?memberships=GS23F006AA',),
                'contract_table': (0, 'h_date_signed', 'desc')
            },
            'membership_pss_541': {
                'tags': ('membership', 'pss'),
                'params': {'args': '013781294', 'test': 'true', 'memberships': 'GS00F238DA'},
                'action': ('#GS00F238DA', 'click'),
                'naics': ('all', 11),
                'membership_filters': (None, 1, 1, 0, {
                    1: ('', '202-962-3955', 'SHERRY.LUPISELLA@720STRATEGIES.COM'),
                }, {
                    1: ('SB',)
                }),
                'vendor_sam': ('6/4/19',),
                'vendor_info': ('720 STRATEGIES, LLC', '013781294', '67PL3', '25', '$7,127,114'),
                'vendor_address': ('1220 19Th St Nw Ste 300', 'Washington, DC 20036', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/013781294/csv/?memberships=GS00F238DA',),
                'contract_table': (0, 'h_date_signed', 'desc')
            },
            'membership_pss_871': {
                'tags': ('membership', 'pss'),
                'params': {'args': '828985940', 'test': 'true', 'memberships': 'GS10F060AA'},
                'action': ('#GS10F060AA', 'click'),
                'naics': ('all', 5),
                'membership_filters': (None, 1, 1, 0, {
                    1: ('', '732-493-1700', 'nmanheimer@aaski.com'),
                }),
                'vendor_sam': ('2/1/19',),
                'vendor_info': ('AASKI TECHNOLOGY INC', '828985940', '59JH6', '417', '$241,837,216'),
                'vendor_address': ('1104 S Philadelphia Blvd #800', 'Aberdeen, MD 21001', True),
                'vendor_badges': (),
                'contract_result_info': ('vendor/828985940/csv/?memberships=GS10F060AA',),
                'contract_table': (1, 'h_date_signed', 'desc')
            },
            'membership_pss_874': {
                'tags': ('membership', 'pss'),
                'params': {'args': '114214211', 'test': 'true', 'memberships': 'GS10F0081V'},
                'action': ('#GS10F0081V', 'click'),
                'naics': ('all', 16),
                'membership_filters': (None, 1, 1, 0, {
                    1: ('', '703-840-3491', 'doc.grantham@6Ksystems.com'),
                }, {
                    1: ('SDB', '8(a)')
                }),
                'vendor_sam': ('6/28/19',),
                'vendor_info': ('6K SYSTEMS, INC.', '114214211', '1ZJK7', '100', '$5,666,666'),
                'vendor_address': ('11710 Plaza America Dr Ste 810', 'Reston, VA 20190', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/114214211/csv/?memberships=GS10F0081V',),
                'contract_table': (3, 'h_date_signed', 'desc')
            },
            'membership_pss_874500': {
                'tags': ('membership', 'pss'),
                'params': {'args': '080117787', 'test': 'true', 'memberships': 'GS00F0005U'},
                'action': ('#GS00F0005U', 'click'),
                'naics': ('all', 11),
                'membership_filters': (None, 1, 1, 0, {
                    1: ('', '478-923-9041', 'ddomingue@advanced-core.com'),
                }, {
                    1: ('SDB', '8(a)')
                }),
                'vendor_sam': ('7/5/19',),
                'vendor_info': ('ADVANCED CORE CONCEPTS, LLC', '080117787', '7JRY5', '30', '$4,900,000'),
                'vendor_address': ('645 Tallulah Trl Ste 201', 'Warner Robins, GA 31088', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/080117787/csv/?memberships=GS00F0005U',),
                'contract_table': (2, 'h_date_signed', 'desc')
            },
            'membership_pss_899': {
                'tags': ('membership', 'pss'),
                'params': {'args': '038523239', 'test': 'true', 'memberships': 'GS10F0175M'},
                'action': ('#GS10F0175M', 'click'),
                'naics': ('all', 7),
                'membership_filters': (None, 1, 1, 0, {
                    1: ('', '907-455-6777', 'tdelong@abrinc.com'),
                }, {
                    1: ('SB',)
                }),
                'vendor_sam': ('11/20/18',),
                'vendor_info': ('ABR INC', '038523239', '0Y330', '49', '$13,967,623'),
                'vendor_address': ('2842 Goldstream Rd', 'Fairbanks, AK 99709', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/038523239/csv/?memberships=GS10F0175M',),
                'contract_table': (5, 'h_date_signed', 'desc', ('Prev', '1'), '2')
            },
            'mixed': {
                'tags': ('naics', 'membership', 'mixed'),
                'params': {'args': '114214211', 'test': 'true', 'memberships': 'GS10F0081V', 'naics': '541611'},
                'action': (('#naics-code', 'select[541611]'), ('#GS10F0081V', 'click')),
                'naics': ('541611', 16),
                'membership_filters': ('GS10F0081V', 1, 1, 0, {
                    1: ('', '703-840-3491', 'doc.grantham@6Ksystems.com')
                }),
                'vendor_sam': ('6/28/19',),
                'vendor_info': ('6K SYSTEMS, INC.', '114214211', '1ZJK7', '100', '$5,666,666'),
                'vendor_address': ('11710 Plaza America Dr Ste 810', 'Reston, VA 20190', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/114214211/csv/?naics=541611&memberships=GS10F0081V',),
                'contract_table': (3, 'h_date_signed', 'desc')
            },
            'sorting': {
                'tags': ('sort',),
                'params': {'args': '129304551', 'test': 'true', 'ordering': '-obligated_amount'},
                'action': ('th.h_value', 'click'),
                'naics': ('all', 15),
                'membership_filters': (None, 2, 0, 0, {
                    2: ('Donald Hill III', '202-434-8470', 'dhill@actionfacilities.com')
                }),
                'vendor_sam': ('1/2/19',),
                'vendor_info': ('ACTION FACILITIES MANAGEMENT, INC.', '129304551', '3EET9', '182', '$14,600,000'),
                'vendor_address': ('115 Malone Dr', 'Morgantown, WV 26501', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/129304551/csv/?ordering=-obligated_amount',),
                'contract_table': (5, 'h_value', 'desc', ('Prev', '1'), '2'),
                'o1|xpath://*[@id="vendor_contracts"]/tbody/tr[2]/td[6]': ('float__is_min', '<<xpath://*[@id="vendor_contracts"]/tbody/tr[3]/td[6]>>'),
                'o2|xpath://*[@id="vendor_contracts"]/tbody/tr[3]/td[6]': ('float__is_min', '<<xpath://*[@id="vendor_contracts"]/tbody/tr[4]/td[6]>>'),
                'o3|xpath://*[@id="vendor_contracts"]/tbody/tr[4]/td[6]': ('float__is_min', '<<xpath://*[@id="vendor_contracts"]/tbody/tr[5]/td[6]>>'),
                'o4|xpath://*[@id="vendor_contracts"]/tbody/tr[5]/td[6]': ('float__is_min', '<<xpath://*[@id="vendor_contracts"]/tbody/tr[6]/td[6]>>'),
            },
            'paging': {
                'tags': ('page',),
                'params': {'args': '008050242', 'test': 'true', 'page': 2},
                'action': ('link_text:2', 'click'),
                'naics': ('all', 27),
                'membership_filters': (None, 2, 0, 2, {
                    1: ('Shelly Bowan', '703-418-0636', 'OASIS@act-i.com'),
                    2: ('Jeff Earley', '703-418-0636', 'OASIS@act-i.com')
                }),
                'vendor_sam': ('2/13/19',),
                'vendor_info': ('ADVANCED CONCEPTS AND TECHNOLOGIES INTERNATIONAL, LLC DBA ACT-I', '008050242', '1C2H1', '55', '$5,400,000'),
                'vendor_address': ('1105 Wooded Acres Ste 500', 'Waco, TX 76710', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/008050242/csv/?page=2',),
                'contract_table': (5, 'h_date_signed', 'desc', ('2', 'Next'), '1'),
            },
            'page_count': {
                'tags': ('page',),
                'params': {'args': '039872622', 'test': 'true', 'count': 3},
                'naics': ('all', 7),
                'membership_filters': (None, 2, 0, 2, {
                    1: ('Lynna S. Hood', '571-257-4785', 'lhood@addxcorp.com'),
                    2: ('Lynna S. Hood', '571-257-4785', 'lhood@addxcorp.com')
                }, {
                    1: ('SB', 'VO', 'SDVO'),
                    2: ('SB', 'VO', 'SDVO')
                }),
                'vendor_sam': ('10/16/18',),
                'vendor_info': ('ADDX CORPORATION', '039872622', '1XPA3', '62', '$16,534,185'),
                'vendor_address': ('4900 Seminary Rd Ste 700', 'Alexandria, VA 22311', True),
                'vendor_badges': (True,),
                'contract_result_info': ('vendor/039872622/csv/?count=3',),
                'contract_table': (3, 'h_date_signed', 'desc', ('Prev', '1'), '4'),
            }
        }
    })
    
    def initialize(self):
        self.path = 'vendor'
