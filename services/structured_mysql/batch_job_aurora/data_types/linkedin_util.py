def resolve_seniority(code):
    strings = code.split(":")
    code = int(strings[len(strings) - 1])
    if code in seniority_codes.keys():
        return seniority_codes[code]
    return code


def resolve_industry(code):
    strings = code.split(":")
    code = int(strings[len(strings)-1])
    if code in industry_codes.keys():
        return industry_codes[code]
    return code


def resolve_function(code):
    strings = code.split(":")
    code = int(strings[len(strings) - 1])
    if code in function_codes.keys():
        return function_codes[code]
    return code


def resolve_region(code):
    strings = code.split(":")
    code = int(strings[len(strings) - 1])
    return code


def resolve_country(code):
    strings = code.split(":")
    code = strings[len(strings) - 1]
    return code


industry_codes = {
    1: "Defense & Space",
    3: "Computer Hardware",
    4: "Computer Software",
    5: "Computer Networking",
    6: "Internet",
    7: "Semiconductors",
    8: "Telecommunications",
    9: "Law Practice",
    10: "Legal Services",
    11: "Management Consulting",
    12: "Biotechnology",
    13: "Medical Practice",
    14: "Hospital & Health Care",
    15: "Pharmaceuticals",
    16: "Veterinary",
    17: "Medical Devices",
    18: "Cosmetics",
    19: "Apparel & Fashion",
    20: "Sporting Goods",
    21: "Tobacco",
    22: "Supermarkets",
    23: "Food Production",
    24: "Consumer Electronics",
    25: "Consumer Goods",
    26: "Furniture",
    27: "Retail",
    28: "Entertainment",
    29: "Gambling & Casinos",
    30: "Leisure, Travel & Tourism",
    31: "Hospitality",
    32: "Restaurants",
    33: "Sports",
    34: "Food & Beverages",
    35: "Motion Pictures and Film",
    36: "Broadcast Media",
    37: "Museums and Institutions",
    38: "Fine Art",
    39: "Performing Arts",
    40: "Recreational Facilities and Services",
    41: "Banking",
    42: "Insurance",
    43: "Financial Services",
    44: "Real Estate",
    45: "Investment Banking",
    46: "Investment Management",
    47: "Accounting",
    48: "Construction",
    49: "Building Materials",
    50: "Architecture & Planning",
    51: "Civil Engineering",
    52: "Aviation & Aerospace",
    53: "Automotive",
    54: "Chemicals",
    55: "Machinery",
    56: "Mining & Metals",
    57: "Oil & Energy",
    58: "Shipbuilding",
    59: "Utilities",
    60: "Textiles",
    61: "Paper & Forest Products",
    62: "Railroad Manufacture",
    63: "Farming",
    64: "Ranching",
    65: "Dairy",
    66: "Fishery",
    67: "Primary/Secondary Education",
    68: "Higher Education",
    69: "Education Management",
    70: "Research",
    71: "Military",
    72: "Legislative Office",
    73: "Judiciary",
    74: "International Affairs",
    75: "Government Administration",
    76: "Executive Office",
    77: "Law Enforcement",
    78: "Public Safety",
    79: "Public Policy",
    80: "Marketing and Advertising",
    81: "Newspapers",
    82: "Publishing",
    83: "Printing",
    84: "Information Services",
    85: "Libraries",
    86: "Environmental Services",
    87: "Package/Freight Delivery",
    88: "Individual & Family Services",
    89: "Religious Institutions",
    90: "Civic & Social Organization",
    91: "Consumer Services",
    92: "Transportation/Trucking/Railroad",
    93: "Warehousing",
    94: "Airlines/Aviation",
    95: "Maritime",
    96: "Information Technology and Services",
    97: "Market Research",
    98: "Public Relations and Communications",
    99: "Design",
    100: "Non-Profit Organization Management",
    101: "Fund-Raising",
    102: "Program Development",
    103: "Writing and Editing",
    104: "Staffing and Recruiting",
    105: "Professional Training & Coaching",
    106: "Venture Capital & Private Equity",
    107: "Political Organization",
    108: "Translation and Localization",
    109: "Computer Games",
    110: "Events Services",
    111: "Arts and Crafts",
    112: "Electrical/Electronic Manufacturing",
    113: "Online Media",
    114: "Nanotechnology",
    115: "Music",
    116: "Logistics and Supply Chain",
    117: "Plastics",
    118: "Computer & Network Security",
    119: "Wireless",
    120: "Alternative Dispute Resolution",
    121: "Security and Investigations",
    122: "Facilities Services",
    123: "Outsourcing/Offshoring",
    124: "Health, Wellness and Fitness",
    125: "Alternative Medicine",
    126: "Media Production",
    127: "Animation",
    128: "Commercial Real Estate",
    129: "Capital Markets",
    130: "Think Tanks",
    131: "Philanthropy",
    132: "E-Learning",
    133: "Wholesale",
    134: "Import and Export",
    135: "Mechanical or Industrial Engineering",
    136: "Photography",
    137: "Human Resources",
    138: "Business Supplies and Equipment",
    139: "Mental Health Care",
    140: "Graphic Design",
    141: "International Trade and Development",
    142: "Wine and Spirits",
    143: "Luxury Goods & Jewelry",
    144: "Renewables & Environment",
    145: "Glass, Ceramics & Concrete",
    146: "Packaging and Containers",
    147: "Industrial Automation",
    148: "Government Relations",
}

function_codes = {
    -1: None,
    1: "Accounting",
    2: "Administrative",
    3: "Arts and Design",
    4: "Business Development",
    5: "Community & Social Services",
    6: "Consulting",
    7: "Education",
    8: "Engineering",
    9: "Entrepreneurship",
    10: "Finance",
    11: "Healthcare Services",
    12: "Human Resources",
    13: "Information Technology",
    14: "Legal",
    15: "Marketing",
    16: "Media & Communications",
    17: "Military & Protective Services",
    18: "Operations",
    19: "Product Management",
    20: "Program & Product Management",
    21: "Purchasing",
    22: "Quality Assurance",
    23: "Real Estate",
    24: "Research",
    25: "Sales",
    26: "Support"
}

seniority_codes = {
    1: "Unpaid",
    2: "Training",
    3: "Entry-level",
    4: "Senior",
    5: "Manager",
    6: "Director",
    7: "Vice President (VP)",
    8: "Chief X Officer (CxO)",
    9: "Partner",
    10: "Owner"
}