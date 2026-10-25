import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_proj.settings')
django.setup()

from restaurant.models import Category, MenuItem, Order, Reservation

def seed_database():
    print("Clearing old data...")
    MenuItem.objects.all().delete()
    Category.objects.all().delete()

    print("Seeding Categories...")
    cat_burgers = Category.objects.create(
        name="Gourmet Burgers",
        name_ar="برجر فاخر",
        icon="fa-burger",
        order=1
    )
    cat_pizzas = Category.objects.create(
        name="Artisanal Pizzas",
        name_ar="بيتزا إيطالية",
        icon="fa-pizza-slice",
        order=2
    )
    cat_grills = Category.objects.create(
        name="Grills & Steaks",
        name_ar="مشاوي وستيك",
        icon="fa-drumstick-bite",
        order=3
    )
    cat_pastas = Category.objects.create(
        name="Pasta & Risotto",
        name_ar="باستا وروبيان",
        icon="fa-utensils",
        order=4
    )
    cat_seafood = Category.objects.create(
        name="Fresh Seafood",
        name_ar="مأكولات بحرية",
        icon="fa-fish",
        order=5
    )
    cat_salads = Category.objects.create(
        name="Salads & Soups",
        name_ar="سلطات وشوربات",
        icon="fa-leaf",
        order=6
    )
    cat_sandwiches = Category.objects.create(
        name="Wraps & Sandwiches",
        name_ar="سندوتشات ورابس",
        icon="fa-bread-slice",
        order=7
    )
    cat_drinks = Category.objects.create(
        name="Craft Drinks",
        name_ar="مشروبات كوكتيل",
        icon="fa-glass-water",
        order=8
    )
    cat_hot_drinks = Category.objects.create(
        name="Hot Beverages",
        name_ar="مشروبات ساخنة",
        icon="fa-mug-hot",
        order=9
    )
    cat_juices = Category.objects.create(
        name="Fresh Juices",
        name_ar="عصائر طبيعية",
        icon="fa-blender",
        order=10
    )
    cat_desserts = Category.objects.create(
        name="Heavenly Desserts",
        name_ar="حلويات غربية",
        icon="fa-cake-candles",
        order=11
    )
    cat_oriental = Category.objects.create(
        name="Oriental Dishes",
        name_ar="أطباق شرقية",
        icon="fa-bowl-rice",
        order=12
    )

    print("Seeding Menu Items...")
    items = [
        # ============ BURGERS ============
        {
            "category": cat_burgers,
            "name": "The Royal Truffle Burger",
            "name_ar": "برجر الترفل الملكي",
            "description": "Double Angus beef patty, black truffle aioli, aged Swiss cheddar, caramelized onions, crisp arugula on a brioche bun.",
            "description_ar": "شريحتان من لحم الأنجوس الفاخر مع مايونيز الترفل الأسود، جبن شيدر سويسري معتق، بصل مكرمل وجرجير طازج في خبز البريوش.",
            "price": 280.00,
            "rating": 4.9,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": False,
            "calories": 780,
            "prep_time_mins": 15,
            "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_burgers,
            "name": "Smoky Jalapeño Smash Burger",
            "name_ar": "سبايسي سماش برجر",
            "description": "Smashed beef patties, smoked bacon jam, fiery jalapeños, melted pepper jack cheese & chipotle sauce.",
            "description_ar": "شرائح برجر مضغوطة بحرفية مع مربى البكون المدخن، هالابينو حار، جبن بيبر جاك وصلصة التشيبوتلي الحارة.",
            "price": 240.00,
            "rating": 4.8,
            "is_popular": True,
            "is_spicy": True,
            "is_vegetarian": False,
            "calories": 820,
            "prep_time_mins": 12,
            "image": "https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_burgers,
            "name": "Avocado Garden Veggie Burger",
            "name_ar": "برجر الخضار والأفوكادو",
            "description": "Plant-based artisanal patty, fresh sliced avocado, sun-dried tomato pesto, lettuce and vegan garlic aioli.",
            "description_ar": "قرص خضروات ومشروم طازج مع شقائق الأفوكادو، بيستو الطماطم المجففة، وثومية نباتية ممتازة.",
            "price": 210.00,
            "rating": 4.7,
            "is_popular": False,
            "is_spicy": False,
            "is_vegetarian": True,
            "calories": 520,
            "prep_time_mins": 15,
            "image": "https://images.unsplash.com/photo-1520072959219-c595dc870360?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_burgers,
            "name": "BBQ Bacon Double Smash",
            "name_ar": "برجر بيكون مزدوج بالبي بي كيو",
            "description": "Two smashed patties, crispy streaky bacon, house BBQ sauce, cheddar cheese, pickles & mustard mayo.",
            "description_ar": "شريحتان مضغوطتان من اللحم مع بيكون مقرمش، صلصة بي بي كيو بيتية، جبن شيدر ومخلل.",
            "price": 260.00,
            "rating": 4.8,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": False,
            "calories": 900,
            "prep_time_mins": 13,
            "image": "https://images.unsplash.com/photo-1586190848861-99aa4a171e90?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_burgers,
            "name": "Classic Wagyu Cheeseburger",
            "name_ar": "برجر واجيو كلاسيك",
            "description": "Premium A5 Wagyu beef patty, American cheese, iceberg lettuce, tomato, house special sauce.",
            "description_ar": "قرص لحم واجيو A5 الياباني الفاخر مع جبن أمريكي وخس طازج وصلصة المطبخ الخاصة.",
            "price": 380.00,
            "rating": 5.0,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": False,
            "calories": 850,
            "prep_time_mins": 18,
            "image": "https://images.unsplash.com/photo-1572802419224-296b0aeee0d9?auto=format&fit=crop&w=800&q=80"
        },

        # ============ PIZZAS ============
        {
            "category": cat_pizzas,
            "name": "Woodfired Truffle & Mushroom Pizza",
            "name_ar": "بيتزا المشروم والترفل",
            "description": "Slow-fermented Neapolitan sourdough dough, wild mushrooms, fresh mozzarella, truffle oil & thyme.",
            "description_ar": "عجينة نابولية مخمرة بحرفية مع فطر عيش الغراب البري، موزاريلا طازجة وزيت الترفل الفاخر والزعتر.",
            "price": 320.00,
            "rating": 5.0,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": True,
            "calories": 890,
            "prep_time_mins": 18,
            "image": "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_pizzas,
            "name": "Diablo Pepperoni & Honey Pizza",
            "name_ar": "بيتزا البيبروني والعسل الحار",
            "description": "Crispy pepperoni cups, hot chili honey drizzle, San Marzano tomato sauce & buffalo mozzarella.",
            "description_ar": "قطع البيبروني المقرمشة مع قطرات العسل الحار، صلصة طماطم سان مارزانو وموزاريلا البوفالو.",
            "price": 290.00,
            "rating": 4.9,
            "is_popular": True,
            "is_spicy": True,
            "is_vegetarian": False,
            "calories": 940,
            "prep_time_mins": 16,
            "image": "https://images.unsplash.com/photo-1628840042765-356cda07504e?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_pizzas,
            "name": "Classic Margherita Supreme",
            "name_ar": "مارجريتا إيطالية أصلية",
            "description": "San Marzano tomatoes, fresh Fior di Latte mozzarella, fragrant basil leaves, and extra virgin olive oil.",
            "description_ar": "طماطم سان مارزانو، جبن فيور دي لاتي، أوراق الريحان الفواحة وزيت الزيتون البكر الممتاز.",
            "price": 230.00,
            "rating": 4.8,
            "is_popular": False,
            "is_spicy": False,
            "is_vegetarian": True,
            "calories": 710,
            "prep_time_mins": 14,
            "image": "https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_pizzas,
            "name": "Four Cheese Bianca Pizza",
            "name_ar": "بيتزا الأربعة جبن",
            "description": "Mozzarella, gorgonzola, fontina, parmesan on a garlic cream base with walnuts and honey.",
            "description_ar": "موزاريلا، جورجونزولا، فونتينا، بارميزان على قاعدة كريمة الثوم مع الجوز والعسل.",
            "price": 310.00,
            "rating": 4.8,
            "is_popular": False,
            "is_spicy": False,
            "is_vegetarian": True,
            "calories": 960,
            "prep_time_mins": 16,
            "image": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_pizzas,
            "name": "BBQ Chicken Ranch Pizza",
            "name_ar": "بيتزا الدجاج بالبي بي كيو",
            "description": "Grilled chicken strips, smoky BBQ sauce, red onions, cheddar & ranch drizzle.",
            "description_ar": "قطع دجاج مشوية مع صلصة بي بي كيو مدخنة، بصل أحمر، جبن شيدر وصلصة رانش.",
            "price": 270.00,
            "rating": 4.7,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": False,
            "calories": 870,
            "prep_time_mins": 17,
            "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=800&q=80"
        },

        # ============ GRILLS & STEAKS ============
        {
            "category": cat_grills,
            "name": "Prime Ribeye Steak 350g",
            "name_ar": "ستيك ريب آي بقر برايم",
            "description": "Charbroiled Black Angus ribeye served with garlic herb butter, roasted asparagus & truffle potato puree.",
            "description_ar": "قطع ريب آي بلاك أنجوس مشوية على الفحم تقدم مع زبدة الأعشاب والثوم، هليون مشوي وبوريه البطاطس بالترفل.",
            "price": 590.00,
            "rating": 5.0,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": False,
            "calories": 950,
            "prep_time_mins": 25,
            "image": "https://images.unsplash.com/photo-1558030006-450675393462?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_grills,
            "name": "Oriental Mixed Grill Platter",
            "name_ar": "طبق مشاوي شرقية مشكلة",
            "description": "Tender lamb chops, shish tawook, kofta skewers charcoal grilled served with saffron rice & tahini.",
            "description_ar": "ريش ضأن طرية، كباب، شيش طاووق وكفتة مشوية على الفحم تقدم مع أرز بالزعفران وصلصة الطحينة.",
            "price": 480.00,
            "rating": 4.9,
            "is_popular": True,
            "is_spicy": True,
            "is_vegetarian": False,
            "calories": 1100,
            "prep_time_mins": 22,
            "image": "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_grills,
            "name": "Grilled Chicken Supreme",
            "name_ar": "دجاج مشوي فاخر",
            "description": "Whole spatchcock chicken marinated 24h in herbs and spices, charcoal grilled to perfection with garlic sauce.",
            "description_ar": "دجاجة كاملة منقوعة 24 ساعة في الأعشاب والتوابل، مشوية على الفحم تقدم مع صلصة الثوم.",
            "price": 320.00,
            "rating": 4.8,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": False,
            "calories": 680,
            "prep_time_mins": 30,
            "image": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?auto=format&fit=crop&w=1600&q=90"
        },
        {
            "category": cat_grills,
            "name": "Lamb Rack Provencal",
            "name_ar": "ريش الضأن بالأعشاب الفرنسية",
            "description": "Frenched rack of lamb crusted with Dijon mustard, herbs de Provence, served with ratatouille.",
            "description_ar": "ريش ضأن مغطاة بخردل ديجون وأعشاب بروفانسال فرنسية مع مقبلات الخضار.",
            "price": 650.00,
            "rating": 5.0,
            "is_popular": False,
            "is_spicy": False,
            "is_vegetarian": False,
            "calories": 780,
            "prep_time_mins": 35,
            "image": "https://images.unsplash.com/photo-1432139555190-58524dae6a55?auto=format&fit=crop&w=800&q=80"
        },

        # ============ PASTAS ============
        {
            "category": cat_pastas,
            "name": "Creamy Tuscan Shrimp Fettuccine",
            "name_ar": "فيتوتشيني بالجمبري وصلصة التوسكان",
            "description": "Fresh handmade fettuccine, jumbo garlic tiger prawns, sun-dried tomatoes, spinach & parmesan cream.",
            "description_ar": "باستا فيتوتشيني طازجة مع جمبري النمر بالثوم، طماطم مجففة، سبانخ وصلصة الكريمة والبارميجانو.",
            "price": 360.00,
            "rating": 4.8,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": False,
            "calories": 840,
            "prep_time_mins": 18,
            "image": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&w=1600&q=90"
        },
        {
            "category": cat_pastas,
            "name": "Rigatoni Bolognese Tradizionale",
            "name_ar": "ريجاتوني بولونيز إيطالي",
            "description": "Slow-simmered beef ragù with red wine, aromatics, fresh herbs, topped with aged Parmigiano Reggiano.",
            "description_ar": "باستا ريجاتوني مع راجو اللحم المطهو ببطء لمدة 6 ساعات، أعشاب إيطالية ورشة بارميجانو ريجانو معتق.",
            "price": 280.00,
            "rating": 4.7,
            "is_popular": False,
            "is_spicy": False,
            "is_vegetarian": False,
            "calories": 760,
            "prep_time_mins": 15,
            "image": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_pastas,
            "name": "Lobster Linguine al Vongole",
            "name_ar": "لينجويني جراد البحر والمحار",
            "description": "Handmade linguine with Canadian lobster tail, Manila clams, white wine garlic butter sauce.",
            "description_ar": "لينجويني مصنوع يدوياً مع ذيل جراد البحر الكندي، المحار، وصلصة الزبدة والثوم والنبيذ الأبيض.",
            "price": 490.00,
            "rating": 5.0,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": False,
            "calories": 720,
            "prep_time_mins": 22,
            "image": "https://images.unsplash.com/photo-1563379926898-05f4575a45d8?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_pastas,
            "name": "Wild Mushroom Risotto",
            "name_ar": "ريزوتو المشروم البري",
            "description": "Arborio rice slow-cooked with porcini and cremini mushrooms, parmesan, truffle oil and thyme.",
            "description_ar": "أرز الأربوريو المطهو ببطء مع مشروم البورشيني والكريميني، بارميزان وزيت الترفل والزعتر.",
            "price": 310.00,
            "rating": 4.8,
            "is_popular": False,
            "is_spicy": False,
            "is_vegetarian": True,
            "calories": 680,
            "prep_time_mins": 25,
            "image": "https://images.unsplash.com/photo-1476124369491-e7addf5db371?auto=format&fit=crop&w=800&q=80"
        },

        # ============ FRESH SEAFOOD ============
        {
            "category": cat_seafood,
            "name": "Grilled Salmon Fillet",
            "name_ar": "فيليه سلمون مشوي",
            "description": "Norwegian salmon fillet with lemon-dill butter, capers, roasted cherry tomatoes & garlic broccolini.",
            "description_ar": "فيليه سلمون نرويجي مع زبدة الليمون والشبت، الكيبر، طماطم كرزية مشوية والبروكلي بالثوم.",
            "price": 420.00,
            "rating": 4.9,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": False,
            "calories": 540,
            "prep_time_mins": 18,
            "image": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_seafood,
            "name": "Seafood Platter Royale",
            "name_ar": "طبق المأكولات البحرية الملكي",
            "description": "King prawns, calamari rings, sea bass fillet, mussels & scallops with three dipping sauces.",
            "description_ar": "جمبري كينج، حلقات كاليماري، فيليه باس البحر، بلح البحر والاسكالوب مع ثلاثة صلصات.",
            "price": 680.00,
            "rating": 5.0,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": False,
            "calories": 720,
            "prep_time_mins": 25,
            "image": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_seafood,
            "name": "Crispy Calamari Fritti",
            "name_ar": "كاليماري مقلي مقرمش",
            "description": "Tender calamari lightly seasoned and fried golden, served with marinara and garlic aioli.",
            "description_ar": "كاليماري طري متبل خفيفاً ومقلي ذهبياً، يقدم مع صلصة المارينارا والثومية.",
            "price": 185.00,
            "rating": 4.7,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": False,
            "calories": 480,
            "prep_time_mins": 10,
            "image": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?auto=format&fit=crop&w=800&q=80"
        },

        # ============ SALADS & SOUPS ============
        {
            "category": cat_salads,
            "name": "Caesar Salad Royale",
            "name_ar": "سيزر سلطة فاخرة",
            "description": "Crisp romaine hearts, house-made Caesar dressing, shaved parmesan, garlic croutons & anchovies.",
            "description_ar": "أوراق رومين طازجة مع صلصة سيزر بيتية، بارميزان مبشور، خبز محمص بالثوم والأنشوجة.",
            "price": 120.00,
            "rating": 4.7,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": False,
            "calories": 380,
            "prep_time_mins": 8,
            "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_salads,
            "name": "Burrata & Heirloom Tomato Salad",
            "name_ar": "سلطة بوراتا وطماطم موروثة",
            "description": "Creamy burrata, heirloom tomatoes, aged balsamic, fresh basil & extra virgin olive oil.",
            "description_ar": "جبن بوراتا كريمي، طماطم ملونة، بلسميك معتق، ريحان طازج وزيت زيتون بكر ممتاز.",
            "price": 145.00,
            "rating": 4.8,
            "is_popular": False,
            "is_spicy": False,
            "is_vegetarian": True,
            "calories": 310,
            "prep_time_mins": 7,
            "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_salads,
            "name": "Roasted Tomato Bisque",
            "name_ar": "شوربة الطماطم المشوية",
            "description": "Slow-roasted vine tomatoes, fresh cream, basil oil, served with parmesan crostini.",
            "description_ar": "طماطم عناقيد مشوية ببطء مع كريمة طازجة وزيت الريحان، تقدم مع خبز محمص بالبارميزان.",
            "price": 90.00,
            "rating": 4.8,
            "is_popular": False,
            "is_spicy": False,
            "is_vegetarian": True,
            "calories": 210,
            "prep_time_mins": 10,
            "image": "https://images.unsplash.com/photo-1547592166-23ac45744acd?auto=format&fit=crop&w=800&q=80"
        },

        # ============ WRAPS & SANDWICHES ============
        {
            "category": cat_sandwiches,
            "name": "Crispy Chicken Club Sandwich",
            "name_ar": "ساندوتش كلوب بالدجاج المقرمش",
            "description": "Golden fried chicken fillet, crispy bacon, lettuce, tomato, cheese & honey mustard sauce.",
            "description_ar": "فيليه دجاج مقلي ذهبي مع بيكون مقرمش، خس، طماطم، جبن وصلصة الخردل بالعسل.",
            "price": 195.00,
            "rating": 4.8,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": False,
            "calories": 720,
            "prep_time_mins": 12,
            "image": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_sandwiches,
            "name": "Spicy Shawarma Wrap",
            "name_ar": "شاورما دجاج حارة",
            "description": "Marinated grilled chicken strips, garlic sauce, pickles, tomatoes, fries wrapped in fresh khubz bread.",
            "description_ar": "شرائح دجاج متبل مشوية مع ثومية، مخلل، طماطم وبطاطس في خبز طازج.",
            "price": 135.00,
            "rating": 4.9,
            "is_popular": True,
            "is_spicy": True,
            "is_vegetarian": False,
            "calories": 620,
            "prep_time_mins": 10,
            "image": "https://images.unsplash.com/photo-1561651823-34feb02250e4?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_sandwiches,
            "name": "Philly Cheesesteak Wrap",
            "name_ar": "رابس فيلي تشيزستيك",
            "description": "Shaved ribeye steak, sautéed peppers & onions, melted provolone cheese in a grilled flour tortilla.",
            "description_ar": "شرائح ريب آي رفيعة مع فلفل وبصل سوتيه، جبن بروفولون ذائب في تورتيلا مشوية.",
            "price": 220.00,
            "rating": 4.7,
            "is_popular": False,
            "is_spicy": False,
            "is_vegetarian": False,
            "calories": 680,
            "prep_time_mins": 15,
            "image": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=800&q=80"
        },

        # ============ ORIENTAL DISHES ============
        {
            "category": cat_oriental,
            "name": "Koshari Egyptian Classic",
            "name_ar": "كشري مصري أصيل",
            "description": "Egypt's national dish: lentils, rice, pasta, crispy fried onions, spicy tomato sauce & vinegar.",
            "description_ar": "الكشري المصري الأصيل بالعدس، الأرز، الماكرونة، البصل المقلي المقرمش والصلصة الحارة والدقة.",
            "price": 65.00,
            "rating": 4.9,
            "is_popular": True,
            "is_spicy": True,
            "is_vegetarian": True,
            "calories": 580,
            "prep_time_mins": 5,
            "image": "https://images.unsplash.com/photo-1546549032-9571cd6b27df?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_oriental,
            "name": "Lamb Molokhia with Rice",
            "name_ar": "ملوخية باللحمة والأرز",
            "description": "Traditional Egyptian molokhia stew with tender braised lamb, served with white rice and bread.",
            "description_ar": "ملوخية مصرية أصلية بالتقلية على الطريقة التقليدية مع لحمة ضأن طرية وأرز أبيض وعيش.",
            "price": 160.00,
            "rating": 4.8,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": False,
            "calories": 640,
            "prep_time_mins": 15,
            "image": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_oriental,
            "name": "Hawawshi Premium",
            "name_ar": "حواوشي فاخر",
            "description": "Spiced minced beef with onions, parsley and peppers baked in crispy local bread.",
            "description_ar": "لحم مفروم متبل بالبصل والبقدونس والفلفل مخبوز في عيش بلدي مقرمش.",
            "price": 120.00,
            "rating": 4.8,
            "is_popular": True,
            "is_spicy": True,
            "is_vegetarian": False,
            "calories": 720,
            "prep_time_mins": 15,
            "image": "https://images.unsplash.com/photo-1482049016688-2d3e1b311543?auto=format&fit=crop&w=800&q=80"
        },

        # ============ CRAFT DRINKS ============
        {
            "category": cat_drinks,
            "name": "Passion Fruit & Mint Mojito",
            "name_ar": "موخيتو الباشن فروت والنعناع",
            "description": "Fresh passion fruit pulp, crushed mint leaves, lime juice, sparkling soda over crushed ice.",
            "description_ar": "باشن فروت طازج مع نعناع أخضر، عصير ليمون، وصودا منعشة مع الثلج المجروش.",
            "price": 95.00,
            "rating": 4.9,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": True,
            "calories": 160,
            "prep_time_mins": 5,
            "image": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_drinks,
            "name": "Strawberry Basil Lemonade",
            "name_ar": "ليمون فراولة بالريحان",
            "description": "Fresh strawberries, hand-squeezed lemons, basil syrup, sparkling water & mint garnish.",
            "description_ar": "فراولة طازجة مع عصير ليمون طازج، شراب الريحان، مياه فوارة ونعناع.",
            "price": 85.00,
            "rating": 4.8,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": True,
            "calories": 140,
            "prep_time_mins": 5,
            "image": "https://images.unsplash.com/photo-1568909344668-6f14a07b56a0?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_drinks,
            "name": "Mango Chilli Margarita Mocktail",
            "name_ar": "ماجريتا المانجو الحار",
            "description": "Fresh mango blend, tajin chili salt rim, lime, agave syrup & sparkling soda.",
            "description_ar": "مانجو طازجة مع جرم التاهين الحار على حافة الكوب، ليمون، شراب الأجاف وصودا.",
            "price": 105.00,
            "rating": 4.7,
            "is_popular": False,
            "is_spicy": True,
            "is_vegetarian": True,
            "calories": 175,
            "prep_time_mins": 5,
            "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_drinks,
            "name": "Watermelon Rose Cooler",
            "name_ar": "مشروب البطيخ والورد",
            "description": "Fresh watermelon juice, rose water, lychee syrup, mint & pink Himalayan salt.",
            "description_ar": "عصير بطيخ طازج مع ماء ورد، شراب اللتشي، نعناع وملح الهيمالايا الوردي.",
            "price": 90.00,
            "rating": 4.8,
            "is_popular": False,
            "is_spicy": False,
            "is_vegetarian": True,
            "calories": 120,
            "prep_time_mins": 5,
            "image": "https://images.unsplash.com/photo-1527661591475-527312dd65f5?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_drinks,
            "name": "Blue Lagoon Mocktail",
            "name_ar": "بلو لاجون موكتيل",
            "description": "Blue curacao syrup, lemonade, pineapple juice, sparkling water & a cherry garnish.",
            "description_ar": "شراب البلو كوراساو، عصير ليمون، عصير أناناس، مياه فوارة وزينة الكرز.",
            "price": 95.00,
            "rating": 4.7,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": True,
            "calories": 155,
            "prep_time_mins": 5,
            "image": "https://images.unsplash.com/photo-1544145945-f90425340c7e?auto=format&fit=crop&w=800&q=80"
        },

        # ============ HOT BEVERAGES ============
        {
            "category": cat_hot_drinks,
            "name": "Iced Spanish Latte Supreme",
            "name_ar": "سبانيش لاتيه بارد",
            "description": "Double shot specialty espresso, sweetened condensed milk, fresh whole milk, served ice cold.",
            "description_ar": "جرعة مضاعفة من قهوة الإسبريسو المختصة مع حليب مكثف محلى وحليب طازج مثلج.",
            "price": 110.00,
            "rating": 4.8,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": True,
            "calories": 280,
            "prep_time_mins": 5,
            "image": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_hot_drinks,
            "name": "Saffron Cardamom Qahwa",
            "name_ar": "قهوة عربية بالزعفران والهيل",
            "description": "Traditional Arabic coffee with premium saffron, green cardamom, served with dates.",
            "description_ar": "قهوة عربية تقليدية مع زعفران فاخر وهيل أخضر، تقدم مع تمر حجوة.",
            "price": 75.00,
            "rating": 4.9,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": True,
            "calories": 80,
            "prep_time_mins": 5,
            "image": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_hot_drinks,
            "name": "Belgian Hot Chocolate",
            "name_ar": "شوكولاتة ساخنة بلجيكية",
            "description": "Rich 70% dark Belgian chocolate melted with steamed whole milk, topped with whipped cream & cocoa.",
            "description_ar": "شوكولاتة بلجيكية داكنة 70% مذابة مع حليب كامل الدسم مبخر، مع كريمة مخفوقة وكاكاو.",
            "price": 95.00,
            "rating": 4.9,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": True,
            "calories": 350,
            "prep_time_mins": 5,
            "image": "https://images.unsplash.com/photo-1542990253-0d0f5be5f0ed?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_hot_drinks,
            "name": "Matcha Oat Latte",
            "name_ar": "ماتشا لاتيه بحليب الشوفان",
            "description": "Ceremonial grade matcha whisked with oat milk, a touch of honey and steamed foam.",
            "description_ar": "ماتشا درجة احتفالية مخفوقة مع حليب الشوفان ولمسة عسل طبيعي وفوم.",
            "price": 100.00,
            "rating": 4.7,
            "is_popular": False,
            "is_spicy": False,
            "is_vegetarian": True,
            "calories": 180,
            "prep_time_mins": 5,
            "image": "https://images.unsplash.com/photo-1515823064-d6e0c04616a7?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_hot_drinks,
            "name": "Karak Chai Masala",
            "name_ar": "شاي كرك بالمسالا",
            "description": "Strong black tea simmered with fresh ginger, cardamom, cinnamon, cloves & evaporated milk.",
            "description_ar": "شاي أسود قوي مطهو مع الزنجبيل الطازج، الهيل، القرفة، الكرنفل وحليب مكثف.",
            "price": 60.00,
            "rating": 4.8,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": True,
            "calories": 140,
            "prep_time_mins": 5,
            "image": "https://images.unsplash.com/photo-1567922045116-2a00fae2ed03?auto=format&fit=crop&w=800&q=80"
        },

        # ============ FRESH JUICES ============
        {
            "category": cat_juices,
            "name": "Fresh Orange & Carrot Sunrise",
            "name_ar": "عصير برتقال وجزر طازج",
            "description": "Cold-pressed navel oranges and organic carrots with a hint of fresh ginger.",
            "description_ar": "برتقال نابل وجزر طبيعي معصور باردًا مع لمسة زنجبيل طازج.",
            "price": 70.00,
            "rating": 4.8,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": True,
            "calories": 120,
            "prep_time_mins": 3,
            "image": "https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_juices,
            "name": "Mango & Pineapple Tropical Blast",
            "name_ar": "عصير مانجو وأناناس استوائي",
            "description": "Fresh ripe mangoes blended with pineapple, coconut cream & a squeeze of lime.",
            "description_ar": "مانجو طازجة ناضجة مخلوطة مع الأناناس، كريمة جوز الهند وعصير ليمون.",
            "price": 85.00,
            "rating": 4.9,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": True,
            "calories": 180,
            "prep_time_mins": 3,
            "image": "https://images.unsplash.com/photo-1534353473418-4cfa6c56fd38?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_juices,
            "name": "Green Detox Boost",
            "name_ar": "عصير خضار أخضر منقي",
            "description": "Spinach, cucumber, green apple, celery, lemon & fresh ginger cold-pressed.",
            "description_ar": "سبانخ، خيار، تفاح أخضر، كرفس، ليمون وزنجبيل طازج معصور باردًا.",
            "price": 90.00,
            "rating": 4.6,
            "is_popular": False,
            "is_spicy": False,
            "is_vegetarian": True,
            "calories": 95,
            "prep_time_mins": 3,
            "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_juices,
            "name": "Fresh Sugarcane Juice",
            "name_ar": "عصير قصب طازج",
            "description": "Freshly pressed sugarcane juice with a hint of lemon and ginger — a Cairo classic.",
            "description_ar": "عصير قصب معصور طازج مع لمسة ليمون وزنجبيل — الكلاسيكية القاهرية.",
            "price": 45.00,
            "rating": 4.9,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": True,
            "calories": 150,
            "prep_time_mins": 3,
            "image": "https://images.unsplash.com/photo-1502741338009-cac2772e18bc?auto=format&fit=crop&w=800&q=80"
        },

        # ============ DESSERTS ============
        {
            "category": cat_desserts,
            "name": "Molten Chocolate Lava Cake",
            "name_ar": "مولتن كيك الشوكولاتة الذائبة",
            "description": "Warm Belgian chocolate cake with a gooey flowing center, served with Madagascar vanilla bean gelato.",
            "description_ar": "كيك شوكولاتة بلجيكية دافئة بحشوة سائلة ذائبة تقدم مع جيلاتو الفانيليا الفاخرة.",
            "price": 160.00,
            "rating": 5.0,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": True,
            "calories": 620,
            "prep_time_mins": 12,
            "image": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_desserts,
            "name": "Classic Italian Tiramisu",
            "name_ar": "تيراميسو إيطالي أصلي",
            "description": "Espresso-soaked savoiardi ladyfingers layered with rich mascarpone cream and dusted with Valrhona cocoa.",
            "description_ar": "بسكويت أصابع الست المغطوس في القهوة مع طبقات كريمة الماسكاربوني الناعمة وكاكاو فالرونا.",
            "price": 140.00,
            "rating": 4.9,
            "is_popular": False,
            "is_spicy": False,
            "is_vegetarian": True,
            "calories": 480,
            "prep_time_mins": 8,
            "image": "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_desserts,
            "name": "Konafa Cream Royale",
            "name_ar": "كنافة كريمة فاخرة",
            "description": "Buttery shredded kunafa dough filled with ashta cream, topped with rose water syrup & pistachios.",
            "description_ar": "كنافة شعرية بالسمن مع عجوة الأشطة وقطر ماء الورد والفستق الحلبي.",
            "price": 120.00,
            "rating": 5.0,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": True,
            "calories": 540,
            "prep_time_mins": 10,
            "image": "https://images.unsplash.com/photo-1519676867240-f03562e64548?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_desserts,
            "name": "Crème Brûlée Classique",
            "name_ar": "كريم برولي كلاسيك",
            "description": "Velvety vanilla bean custard with a perfectly caramelized sugar crust, served chilled.",
            "description_ar": "كاسترد فانيليا مخملي مع قشرة سكر مكرملة بشكل مثالي، يقدم بارداً.",
            "price": 135.00,
            "rating": 4.9,
            "is_popular": False,
            "is_spicy": False,
            "is_vegetarian": True,
            "calories": 420,
            "prep_time_mins": 5,
            "image": "https://images.unsplash.com/photo-1470124182917-cc6e71b22ecc?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_desserts,
            "name": "Umm Ali Egyptian Bread Pudding",
            "name_ar": "أم علي بالمكسرات",
            "description": "Traditional Egyptian Umm Ali with puff pastry, warm milk, cream, mixed nuts & raisins.",
            "description_ar": "أم علي المصرية التقليدية بعجين الفطير، الحليب الساخن، الكريمة، المكسرات المشكلة والزبيب.",
            "price": 100.00,
            "rating": 4.8,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": True,
            "calories": 580,
            "prep_time_mins": 15,
            "image": "https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?auto=format&fit=crop&w=800&q=80"
        },
        {
            "category": cat_desserts,
            "name": "New York Cheesecake Berry Coulis",
            "name_ar": "تشيزكيك نيويورك بالتوت",
            "description": "Dense and creamy NY-style cheesecake on a graham cracker crust with mixed berry coulis.",
            "description_ar": "تشيزكيك نيويورك كثيف وكريمي على قاعدة بسكويت مع صلصة التوت المشكل.",
            "price": 150.00,
            "rating": 4.9,
            "is_popular": True,
            "is_spicy": False,
            "is_vegetarian": True,
            "calories": 550,
            "prep_time_mins": 5,
            "image": "https://images.unsplash.com/photo-1565958011703-44f9829ba187?auto=format&fit=crop&w=800&q=80"
        },
    ]

    for item_data in items:
        MenuItem.objects.create(**item_data)

    print(f"✅ Successfully seeded {Category.objects.count()} categories and {MenuItem.objects.count()} menu items!")
    print("\n📊 Summary:")
    for cat in Category.objects.all():
        print(f"  - {cat.name}: {cat.items.count()} items")

if __name__ == '__main__':
    seed_database()
