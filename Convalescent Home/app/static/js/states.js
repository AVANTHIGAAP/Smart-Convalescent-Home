
		function populate(s1,s2,a,b){
			var s1=document.getElementById(s1);
			var s2=document.getElementById(s2);
			s2.innerHTML="";
			if(a!='null' && b!= 'null'){
				s1.value = a;
			}
			if(s1.value == "AndhraPradesh"){
				var optionArray=["|--SELECT--","Anantapur|Anantapur","Chittoor|Chittoor","Kakinada|Kakinada","Guntur|Guntur","Ongole|Ongole","Nellore|Nellore","Visakhapatnam|Visakhapatnam","Vijayawada|Vijayawada","Kadapa|Kadapa"]
			}
			if(s1.value == "ArunachalPradesh"){
				var optionArray=["|--SELECT--","Anjaw|Anjaw","Changlang|Changlang","East Siang|East Siang","Kurung Kumey|Kurung Kumey","Lohit|Lohit","Lower Dibang Valley|Lower Dibang Valley","Lower Subansiri|Lower Subansiri","Papum Pare|Papum Pare","Tawang|Tawang","Tirap|Tirap"]
			}
			
			if(s1.value == "Assam"){
				var optionArray=["|--SELECT--","Baksa|Baksa","Barpeta|Barpeta","Bongaigaon|Bongaigaon","Cachar|Cachar","Chirang|Chirang","Darrang|Darrang","Dhemaji|Dhemaji","Dima Hasao|Dima Hasao","Dhubri|Dhubri","Dibrugarh|Dibrugarh","Goalpara|Goalpara","Golaghat|Golaghat"]
			}
			
			if(s1.value == "Bihar"){
				var optionArray=["|--SELECT--","Araria|Araria","Arwal|Arwal","Aurangabad|Aurangabad","Banka|Banka","Begusarai|Begusarai","Bhagalpur|Bhagalpur","Bhojpur|Bhojpur","Buxar|Buxar","Darbhanga|Darbhanga","East Champaran|East Champaran","Gaya|Gaya","Gopalganj|Gopalganj"]

			}
			
			if(s1.value == "Gujarat"){
				var optionArray=["|--SELECT--","Ahmedabad|Ahmedabad","Amreli district|Amreli district","Anand|Anand","Banaskantha|Banaskantha","Bharuch|Bharuch","Bhavnagar|Bhavnagar","Dahod|Dahod","The Dangs|The Dangs","Gandhinagar|Gandhinagar","Jamnagar|Jamnagar","Junagadh|Junagadh","Kutch|Kutch","Kheda|Kheda","Mehsana|Mehsana","Narmada|Narmada","Navsari|Navsari","Patan|Patan","Panchmahal|Panchmahal","Porbandar|Porbandar","Rajkot|Rajkot","Sabarkantha|Sabarkantha","Surendranagar|Surendranagar","Surat|Surat","Vyara|Vyara","Vadodara|Vadodara","Valsad|Valsad"]

			}
			if(s1.value == "Haryana"){
				var optionArray=["|--SELECT--","Ambala|Ambala","Bhiwani|Bhiwani","Faridabad|Faridabad","Fatehabad|Fatehabad","Gurgaon|Gurgaon","Hissar|Hissar","Jhajjar|Jhajjar","Jind|Jind","Karnal|Karnal","Kaithal|Kaithal","Kurukshetra|Kurukshetra","Mahendragarh|Mahendragarh","Mewat|Mewat","Palwal|Palwal","Panchkula|Panchkula","Panipat|Panipat","Rewari|Rewari","Rohtak|Rohtak","Sirsa|Sirsa","Sonipat|Sonipat","Yamuna Nagar|Yamuna Nagar"]

			}
			if(s1.value == "HimachalPradesh"){
				var optionArray=["|--SELECT--","Bilaspur|Bilaspur","Chamba|Chamba","Hamirpur|Hamirpur","Kangra|Kangra","Kinnaur|Kinnaur","Kullu|Kullu","Lahaul and Spiti|Lahaul and Spiti","Mandi|Mandi","Shimla|Shimla","Sirmaur|Sirmaur","Solan|Solan","Una|Una"]

			}
			if(s1.value == "JammuandKashmir"){
				var optionArray=["|--SELECT--","Anantnag|Anantnag","Badgam|Badgam","Bandipora|Bandipora","Baramulla|Baramulla","Doda|Doda","Ganderbal|Ganderbal","Jammu|Jammu","Kargil|Kargil","Kathua|Kathua","Kishtwar|Kishtwar","Kupwara|Kupwara","Kulgam|Kulgam","Leh|Leh","Poonch|Poonch","Pulwama|Pulwama","Rajauri|Rajauri","Ramban|Ramban","Reasi|Reasi","Samba|Samba","Shopian|Shopian","Srinagar|Srinagar","Udhampur|Udhampur"]
			}
			if(s1.value == "Jharkhand"){
				var optionArray=["|--SELECT--","Bokaro|Bokaro","Chatra|Chatra","Deoghar|Deoghar","Dhanbad|Dhanbad","Dumka|Dumka","East Singhbhum|East Singhbhum","Garhwa|Garhwa","Giridih|Giridih","Godda|Godda","Gumla|Gumla","Hazaribag|Hazaribag","Jamtara|Jamtara","Khunti|Khunti","Koderma|Koderma","Latehar|Latehar","Lohardaga|Lohardaga","Pakur|Pakur","Palamu|Palamu","Ramgarh|Ramgarh","Ranchi|Ranchi","Sahibganj|Sahibganj","Seraikela Kharsawan|Seraikela Kharsawan","Simdega|Simdega","West Singhbhum|West Singhbhum"]
			}
			if(s1.value == "Karnataka"){
				var optionArray=["|--SELECT--","Bagalkot|Bagalkot","Bangalore Rural|Bangalore Rural","Bangalore Urban|Bangalore Urban","Belgaum|Belgaum","Bellary|Bellary","Bidar|Bidar","Bijapur|Bijapur","Chamarajnagar|Chamarajnagar","Chikkamagaluru|Chikkamagaluru","Chikkaballapur|Chikkaballapur","Chitradurga|Chitradurga","Davanagere|Davanagere","Dharwad|Dharwad","Dakshina Kannada|Dakshina Kannada","Gadag|Gadag","Gulbarga|Gulbarga","Hassan|Hassan","Haveri district|Haveri district","Kodagu|Kodagu","Kolar|Kolar","Koppal|Koppal","Mandya|Mandya","Mysore|Mysore","Raichur|Raichur","Shimoga|Shimoga","Tumkur|Tumkur","Udupi|Udupi","Uttara Kannada|Uttara Kannada","Ramanagara|Ramanagara","Yadgir|Yadgir"]

			}
			if(s1.value == "Kerala"){
				var optionArray=["|--SELECT--","Alappuzha|Alappuzha","Ernakulam|Ernakulam","Idukki|Idukki","Kannur|Kannur","Kasaragod|Kasaragod","Kollam|Kollam","Kottayam|Kottayam","Kozhikode|Kozhikode","Malappuram|Malappuram","Palakkad|Palakkad","Pathanamthitta|Pathanamthitta","Thrissur|Thrissur","Thiruvananthapuram|Thiruvananthapuram","Wayanad|Wayanad"]
			}
			if(s1.value == "MadhyaPradesh"){
				var optionArray=["|--SELECT--","Alirajpur|Alirajpur","Anuppur|Anuppur","Ashok Nagar|Ashok Nagar","Balaghat|Balaghat","Barwani|Barwani","Betul|Betul","Bhind|Bhind","Bhopal|Bhopal","Burhanpur|Burhanpur","Chhatarpur|Chhatarpur","Chhindwara|Chhindwara","Damoh|Damoh","Datia|Datia","Dewas|Dewas","Dhar|Dhar","Dindori|Dindori","Guna|Guna","Gwalior|Gwalior","Harda|Harda","Hoshangabad|Hoshangabad","Indore|Indore","Jabalpur|Jabalpur","Jhabua|Jhabua","Katni|Katni","Khandwa (East Nimar)|Khandwa (East Nimar)","Khargone (West Nimar)|Khargone (West Nimar)","Mandla|Mandla","Mandsaur|Mandsaur","Morena|Morena","Narsinghpur|Narsinghpur","Neemuch|Neemuch","Panna|Panna","Rewa|Rewa","Rajgarh|Rajgarh","Ratlam|Ratlam","Raisen|Raisen","Sagar|Sagar","Satna|Satna","Sehore|Sehore","Seoni|Seoni","Shahdol|Shahdol","Shajapur|Shajapur","Sheopur|Sheopur","Shivpuri|Shivpuri","Sidhi|Sidhi","Singrauli|Singrauli","Tikamgarh|Tikamgarh","Ujjain|Ujjain","Umaria|Umaria","Vidisha|Vidisha"]
			}
			if(s1.value == "Maharashtra"){
				var optionArray=["|--SELECT--","Ahmednagar|Ahmednagar","Akola|Akola","Amravati|Amravati","Aurangabad|Aurangabad","Bhandara|Bhandara","Beed|Beed","Buldhana|Buldhana","Chandrapur|Chandrapur","Dhule|Dhule","Gadchiroli|Gadchiroli","Gondia|Gondia","Hingoli|Hingoli","Jalgaon|Jalgaon","Jalna|Jalna","Kolhapur|Kolhapur","Latur|Latur","Mumbai City|Mumbai City","Mumbai suburban|Mumbai suburban","Nandurbar|Nandurbar","Nanded|Nanded","Nagpur|Nagpur","Nashik|Nashik","Osmanabad|Osmanabad","Parbhani|Parbhani","Pune|Pune","Raigad|Raigad","Ratnagiri|Ratnagiri","Sindhudurg|Sindhudurg","Sangli|Sangli","Solapur|Solapur","Satara|Satara","Thane|Thane","Wardha|Wardha","Washim|Washim","Yavatmal|Yavatmal"]

			}
			if(s1.value == "Manipur"){
				var optionArray=["|--SELECT--","Bishnupur|Bishnupur","Churachandpur|Churachandpur","Chandel|Chandel","Imphal East|Imphal East","Senapati|Senapati","Tamenglong|Tamenglong","Thoubal|Thoubal","Ukhrul|Ukhrul","Imphal West|Imphal West"]
			}
			if(s1.value == "Meghalaya"){
				var optionArray=["|--SELECT--","East Garo Hills|East Garo Hills","East Khasi Hills|East Khasi Hills","Jaintia Hills|Jaintia Hills","Ri Bhoi|Ri Bhoi","South Garo Hills|South Garo Hills","West Garo Hills|West Garo Hills","West Khasi Hills|West Khasi Hills"]
			}
			if(s1.value == "Mizoram"){
				var optionArray=["|--SELECT--","Aizawl|Aizawl","Champhai|Champhai","Kolasib|Kolasib","Lawngtlai|Lawngtlai","Lunglei|Lunglei","Mamit|Mamit","Saiha|Saiha","Serchhip|Serchhip"]

			}
			if(s1.value == "Nagaland"){
				var optionArray=["|--SELECT--","Dimapur|Dimapur","Kohima|Kohima","Mokokchung|Mokokchung","Mon|Mon","Phek|Phek","Tuensang|Tuensang","Wokha|Wokha","Zunheboto|Zunheboto"]

			}
			if(s1.value == "Orissa"){
				var optionArray=["|--SELECT--","Angul|Angul","Boudh (Bauda)|Boudh (Bauda)","Bhadrak|Bhadrak","Balangir|Balangir","Bargarh (Baragarh)|Bargarh (Baragarh)","Balasore|Balasore","Cuttack|Cuttack","Debagarh (Deogarh)|Debagarh (Deogarh)","Dhenkanal|Dhenkanal","Ganjam|Ganjam","Gajapati|Gajapati","Jharsuguda|Jharsuguda","Jajpur|Jajpur","Jagatsinghpur|Jagatsinghpur","Khordha|Khordha","Kendujhar (Keonjhar)|Kendujhar (Keonjhar)","Kalahandi|Kalahandi","Kandhamal|Kandhamal","Koraput|Koraput","Kendrapara|Kendrapara","Malkangiri|Malkangiri","Mayurbhanj|Mayurbhanj","Nabarangpur|Nabarangpur","Nuapada|Nuapada","Nayagarh|Nayagarh","Puri|Puri","Rayagada|Rayagada","Sambalpur|Sambalpur","Subarnapur (Sonepur)|Subarnapur (Sonepur)","Sundergarh|Sundergarh"]

			}
			if(s1.value == "Punjab"){
				var optionArray=["|--SELECT--","Amritsar|Amritsar","Barnala|Barnala","Bathinda|Bathinda","Firozpur|Firozpur","Faridkot|Faridkot","Fatehgarh Sahib|Fatehgarh Sahib","Fazilka|Fazilka","Gurdaspur|Gurdaspur","Hoshiarpur|Hoshiarpur","Jalandhar|Jalandhar","Kapurthala|Kapurthala","Ludhiana|Ludhiana","Mansa|Mansa","Moga|Moga","Sri Muktsar Sahib|Sri Muktsar Sahib","Pathankot|Pathankot","Patiala|Patiala","Rupnagar|Rupnagar","Ajitgarh (Mohali)|Ajitgarh (Mohali)","Sangrur|Sangrur","Nawanshahr|Nawanshahr","Tarn Taran|Tarn Taran"]

			}
			if(s1.value == "Rajasthan"){
				var optionArray=["|--SELECT--","Ajmer|Ajmer","Alwar|Alwar","Bikaner|Bikaner","Barmer|Barmer","Banswara|Banswara","Bharatpur|Bharatpur","Baran|Baran","Bundi|Bundi","Bhilwara|Bhilwara","Churu|Churu","Chittorgarh|Chittorgarh","Dausa|Dausa","Dholpur|Dholpur","Dungapur|Dungapur","Ganganagar|Ganganagar","Hanumangarh|Hanumangarh","Jhunjhunu|Jhunjhunu","Jalore|Jalore","Jodhpur|Jodhpur","Jaipur|Jaipur","Jaisalmer|Jaisalmer","Jhalawar|Jhalawar","Karauli|Karauli","Kota|Kota","Nagaur|Nagaur","Pali|Pali","Pratapgarh|Pratapgarh","Rajsamand|Rajsamand","Sikar|Sikar","Sawai Madhopur|Sawai Madhopur","Sirohi|Sirohi","Tonk|Tonk","Udaipur|Udaipur"]

			}
			if(s1.value == "Sikkim"){
				var optionArray=["|--SELECT--","East Sikkim|East Sikkim","North Sikkim|North Sikkim","South Sikkim|South Sikkim","West Sikkim|West Sikkim"]

			}
			if(s1.value == "TamilNadu"){
				var optionArray=["|--SELECT--","Ariyalur|Ariyalur","Chennai|Chennai","Coimbatore|Coimbatore","Cuddalore|Cuddalore","Dharmapuri|Dharmapuri","Dindigul|Dindigul","Erode|Erode","Kanchipuram|Kanchipuram","Kanyakumari|Kanyakumari","Karur|Karur","Madurai|Madurai","Nagapattinam|Nagapattinam","Nilgiris|Nilgiris","Namakkal|Namakkal","Perambalur|Perambalur","Pudukkottai|Pudukkottai","Ramanathapuram|Ramanathapuram","Salem|Salem","Sivaganga|Sivaganga","Tirupur|Tirupur","Tiruchirappalli|Tiruchirappalli","Theni|Theni","Tirunelveli|Tirunelveli","Thanjavur|Thanjavur","Thoothukudi|Thoothukudi","Tiruvallur|Tiruvallur","Tiruvarur|Tiruvarur","Tiruvannamalai|Tiruvannamalai","Vellore|Vellore","Viluppuram|Viluppuram","Virudhunagar|Virudhunagar"]

			}
			if(s1.value == "Telangana"){
				var optionArray=["|--SELECT--","Adilabad|Adilabad","Hyderabad|Hyderabad","Karimnagar|Karimnagar","Nalgonda|Nalgonda|","Nizamabad|Nizamabad","Warangal|Warangal"]

			}
			if(s1.value == "Tripura"){
				var optionArray=["|--SELECT--","Dhalai|Dhalai","North Tripura|North Tripura","South Tripura|South Tripura","Khowai|Khowai","West Tripura|West Tripura"]

			}
			if(s1.value == "UttarPradesh"){
				var optionArray=["|--SELECT--","Agra|Agra","Allahabad|Allahabad","Aligarh|Aligarh","Ambedkar Nagar|Ambedkar Nagar","Auraiya|Auraiya","Azamgarh|Azamgarh","Barabanki|Barabanki","Budaun|Budaun","Bagpat|Bagpat","Bahraich|Bahraich","Bijnor|Bijnor","Ballia|Ballia","Banda|Banda","Balrampur|Balrampur","Bareilly|Bareilly","Basti|Basti","Bulandshahr|Bulandshahr","Chandauli|Chandauli","Chhatrapati Shahuji Maharaj Nagar|Chhatrapati Shahuji Maharaj Nagar","Chitrakoot|Chitrakoot","Deoria|Deoria","Etah|Etah","Kanshi Ram Nagar|Kanshi Ram Nagar","Etawah|Etawah","Firozabad|Firozabad","Farrukhabad|Farrukhabad","Fatehpur|Fatehpur","Faizabad|Faizabad","Gautam Buddh Nagar|Gautam Buddh Nagar","Gonda|Gonda","Ghazipur|Ghazipur","Gorakhpur|Gorakhpur","Ghaziabad|Ghaziabad","Hamirpur|Hamirpur","Hardoi|Hardoi","Mahamaya Nagar|Mahamaya Nagar","Jhansi|Jhansi","Jalaun|Jalaun","Jyotiba Phule Nagar|Jyotiba Phule Nagar","Jaunpur district|Jaunpur district","Ramabai Nagar (Kanpur Dehat)|Ramabai Nagar (Kanpur Dehat)","Kannauj|Kannauj","Kanpur|Kanpur","Kaushambi|Kaushambi","Kushinagar|Kushinagar","Lalitpur|Lalitpur","Lakhimpur Kheri|Lakhimpur Kheri","Lucknow|Lucknow","Mau|Mau","Meerut|Meerut","Maharajganj|Maharajganj","Mahoba|Mahoba","Mirzapur|Mirzapur","Moradabad|Moradabad","Mainpuri|Mainpuri","Mathura|Mathura","Muzaffarnagar|Muzaffarnagar","Panchsheel Nagar district (Hapur)|Panchsheel Nagar district (Hapur)","Pilibhit|Pilibhit","Shamli|Shamli","Pratapgarh|Pratapgarh","Rampur|Rampur","Raebareli|Raebareli","Saharanpur|Saharanpur","Sitapur|Sitapur","Shahjahanpur|Shahjahanpur","Sant Kabir Nagar|Sant Kabir Nagar","Siddharthnagar|Siddharthnagar","Sonbhadra|Sonbhadra","Sant Ravidas Nagar|Sant Ravidas Nagar","Sultanpur|Sultanpur","Shravasti|Shravasti","Unnao|Unnao","Varanasi|Varanasi"]
			}
			if(s1.value == "Uttarakhand"){
				var optionArray=["|--SELECT--","Almora|Almora","Bageshwar|Bageshwar","Chamoli|Chamoli","Champawat|Champawat","Dehradun|Dehradun","Haridwar|Haridwar","Nainital|Nainital","Pauri Garhwal|Pauri Garhwal","Pithoragarh|Pithoragarh","Rudraprayag|Rudraprayag","Tehri Garhwal|Tehri Garhwal","Udham Singh Nagar|Udham Singh Nagar","Uttarkashi|Uttarkashi"]

			}
			if(s1.value == "WestBengal"){
				var optionArray=["|--SELECT--","Birbhum|Birbhum","Bankura|Bankura","Bardhaman|Bardhaman","Darjeeling|Darjeeling","Dakshin Dinajpur|Dakshin Dinajpur","Hooghly|Hooghly","Howrah|Howrah","Jalpaiguri|Jalpaiguri","Cooch Behar|Cooch Behar","Kolkata|Kolkata","Maldah|Maldah","Paschim Medinipur|Paschim Medinipur","Purba Medinipur|Purba Medinipur","Murshidabad|Murshidabad","Nadia|Nadia","North 24 Parganas|North 24 Parganas","South 24 Parganas|South 24 Parganas","Purulia|Purulia","Uttar Dinajpur|Uttar Dinajpur"]
			}
			for (var option in optionArray) {
				var pair = optionArray[option].split("|");
				var newOption = document.createElement("option");
				newOption.value=pair[0];
				newOption.innerHTML=pair[1];				
				s2.options.add(newOption);
			}
			if(a!='null' && b!= 'null'){
				s2.value = b;
			}
		}
	