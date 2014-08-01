import pickle, random

dictVerbToSentences = dict()

#----------------- argue -----------------
dictVerbToSentences["argue"] = []

dictVerbToSentences["argue"].append([r"Nellie was in the kitchen , had just come to work , when she heard Tim arguing with Julia in the living room .",
r"Although the United States and the U.S.S.R. have been arguing whether there shall be four , five or six top assistants , the most important element in the situation is not the number of deputies but the manner in which these deputies are to do their work .",])

dictVerbToSentences["argue"].append([r"For example , in Burma and Ceylon many Buddhists argue that Buddhism ought to be the official state religion .",
r"Social WorkHuman Service Academic Programs & Development -LRB- edit -RRB- Chenault and Burnford argued that human services programs must educate and train students at the graduate or postgraduate level if human services hoped to be considered a professional discipline .",
r"-LRB- Qualitative Thought 1930 -RRB- Louis Menand argues in The Metaphysical Club that Jane Addams had been critical of Dewey 's emphasis on antagonism in the context of a discussion of the Pullman strike of 1894 .",])

#----------------- base -----------------
dictVerbToSentences["base"] = []

dictVerbToSentences["base"].append([r"School for Conflict Analysis and ResolutionFrom Wikipedia , the free encyclopediaThe School for Conflict Analysis and Resolution -LRB- S-CAR -RRB- EstablishedThe School for Conflict Analysis and Resolution -LRB- S-CAR -RRB- is a division of George Mason University based near Washington and D.C. and United States with locations in Arlington and Fairfax , and Lorton and Virginia .",
r"The architect Eero Saarinen , based in Birmingham and Michigan , created one of the early master plans for North Campus and designed several of its buildings in the 1950s , including the Earl V. Moore School of Music Building .",])

dictVerbToSentences["base"].append([r"The Center for Universal Design at NCSU established a set of Principles of Universal Design based on UD to guide and evaluate the design process , with a goal toward creating more accessible products and environments .",
r"The Academic Bill of Rights is based on the Declaration of Principles on Academic Freedom and Academic Tenure as published by the American Association of University Professors in 1915 , and modified in 1940 and 1970 .",])

#----------------- be -----------------
dictVerbToSentences["be"] = []

dictVerbToSentences["be"].append([r"The Fine Arts Center is home to the School of Art and houses classrooms , a studio , workshop spaces , art galleries a glassblowing studio and faculty offices .",
r"Parkview Campus -LRB- edit -RRB- College of Engineering and Applied Sciences , Parkview CampusThe Parkview Campus is home to the University 's College of Engineering and Applied Sciences and the Business Technology and Research Park .",
r"The $ 11 million Parma Payne Goodall Alumni Center opened in October 2009 and is home to the SDSU Alumni Association and the Campanile Foundation .",
r"Completed and reopened in March 2007 , Morrill Hall is home to the Christian Petersen Art Museum .",
r"In research , UAMS is well known as a leader in multiple myeloma , geriatrics , vision , and spine treatment research and is home to the Arkansas Biosciences Institute and the UAMS Bioventures Business Incubator .",
r"UAMS is also home to 240 physicians featured in the list of Best Doctors in America , some of which are at Arkansas Children 's Hospital and Central Arkansas Veteran 's Healthcare System , where UAMS faculty serve as staff .",
r"Among notable alumni are Neil Armstrong , the first human to step on the moon ; George Lucas , creator of the Star Wars trilogy ; Hollywood screen legend John Wayne -LRB- who also played in the USC football team -RRB- ; world-renowned architect Frank Gehry ; and deposed Egyptian president Mohamed Morsi , the first democratically-elected president in that country 's history .",
r"Salem College is home to the Salem College Center for Women Writers .",
r"The Ambler campus Ambler College , which is home to the Community and Regional Planning , Landscape Architecture , and Horticulture Departments , has changed their name in 2009 to the School of Environmental Design , due to the campus focus on environmental sustainability .",])

dictVerbToSentences["be"].append([r"You remember the words of President Kennedy a week or so ago , when someone asked him when he was in Canada , and Dean Rusk was in Europe , and Vice President Johnson was in Asia , `` Who is running the store '' ?",
r"Today , M. Kegham was in Detroit , en route to join his wife and children in California .",
r"Mr. Hammarskjold was in Africa on a mission of peace .",
r"-LRB- citation needed -RRB- However , it should be noted that John Dewey was in China in the early 1900s and his ideas were extremely popular .",
r"Last summer John and Elizabeth Sherrill were in Alaska .",])

#----------------- begin -----------------
dictVerbToSentences["begin"] = []

dictVerbToSentences["begin"].append([r"Best Fest and Fiesta UTSA -LRB- edit -RRB- The 2013 Fiesta UTSAFiesta UTSA , an annual event held in April , began in 1978 .",
r"Best Fest , an annual celebration held in October , began in 1978 -LRB- as `` Bestfest '' -RRB- as `` a special salute to five of the state 's outstanding festivals , '' including New Braunfels 's Wurstfest , Corpus Christi 's Buccaneer Days , San Antonio 's Fiesta , the Texas State Fair in Dallas , and George Washington 's Birthday Celebration in Laredo .",
r"In 2012 , University College London began its interdisciplinary Arts and Sciences BASc degree -LRB- which has kinship with the liberal arts model -RRB- with 80 students .",
r"Athens State University began as the Athens Female Academy in 1822 .",
r"In 1908 , the State legislature began the NY State College of Agriculture at Alfred University .",
r"Classes began in the Correll Science Complex in January 2009 .",
r"The University began in earnest in 1925 when George E. Merrick , the founder of Coral Gables , gave 160 acres -LRB- 0.6 -RRB- and nearly $ 5 , -LRB- $ 67.2 million , adjusted for current inflation -RRB- to the effort .",])

dictVerbToSentences["begin"].append([r"Roberta and Dave began to back toward the door .",
r"These were carried out not too faithfully by Filippo Costaggini , who began by supplying the missing member to the founder of Pennsylvania and noting in pencil , in Italian , that he `` began at this point '' .",
r"That finished the job that Captain Chandler and Lieutenant Carroll had begun .",])

#----------------- bring -----------------
dictVerbToSentences["bring"] = []

dictVerbToSentences["bring"].append([r"Barton was relieved to see that Carl Dill and Emmett Foster had brought extra mounts .",
r"It stands in the middle of what was once the Forum of Constantine , who brought it from Rome .",
r"The Alabamas brought in annually 15,000 to 20,000 deerskins , and the Choctaws and Chickasaws brought the total up to 50,000 pelts .",])

dictVerbToSentences["bring"].append([r"With that possibility in mind , Arkansas ' Wilbur Mills deliberately delayed calling a meeting of the Committee on Committees , and coolheaded Democrats sought to bring Rayburn and Smith together again to work out some sort of face-saving compromise .",
r"Mercer 's Whiteman association brought him into contact with Hoagy Carmichael , whose `` Snowball '' Mercer relyriced as `` Lazybones '' , in which form it became a hit and marked the real beginning of Mercer 's song-writing career .",])

#----------------- call -----------------
dictVerbToSentences["call"] = []

dictVerbToSentences["call"].append([r"when his Holiness Pope John 23 , first called for an Ecumenical Council , and at the same time voiced his yearning for Christian unity , the enthusiasm among Catholic and Protestant ecumenicists was immediate .",
r"The infamous Wansee Conference called by Heydrich in January 1942 , to organize the material and technical means to put to death the eleven million Jews spread throughout the nations of Europe , was attended by representatives of major organs of the German state , including the Reich Minister of the Interior , the State Secretary in charge of the Four Year Plan , the Reich Minister of Justice , the Under Secretary of Foreign Affairs .",])

dictVerbToSentences["call"].append([r"Simply call Mr. Whipsnade Oscar , and Dr. Dunne P. GA , and C'un Major Frank .",
r"Afterwards I learned that Eileen had called Thelma on the telephone and made a big scene about Thelma trying to take her husband away .",
r"After supper , Doc called Whitey Gresham , who was now a lieutenant and had a family .",
r"Maybe I could call Rimanelli at the magazine Rottosei where he worked .",])

dictVerbToSentences["call"].append([r"A Sonata For Violin And Piano , called `` Bella Bella '' , by Robert Fleming , was given its first United States performance .",
r"One who , for a time , succeeded best and was still the sorriest of all was Charles Arthur Shires , who called himself , in the newspapers , Art the Great , or The Great Shires .",
r"Other hitters bloomed with more or less vigor in the news and a few even dared to dream of matching Ruth , who was still called Jidge by all his friends , or Leo or Two-Head by those who dared to taunt him -LRB- Leo was the name of the ball player he liked the least -RRB- and who called most of the world `` Kid '' .",
r"Main article : Backward designUnderstanding by Design relies on what Wiggins and McTighe call `` backward design '' -LRB- also known as `` backwards planning '' -RRB- .",
r"-LRB- July 2013 -RRB- Campbell University was founded as a community school on January 5 , 1887 called Buies Creek Academy .",
r"In 1900 , the Academy of the Incarnate Word , which had been established first in an area of San Antonio called Government Hill , was moved to the Motherhouse of the Sisters of Charity of the Incarnate Word in Alamo Heights .",
r"Identification with the Christian right -LRB- edit -RRB- In 1995 , Harvey Cox , the liberal Harvard theologian , wrote that Regent has been called `` the Harvard of the Christian Right '' and noted that `` Regent , it appears , is not so much a boot camp for rightist cadres as a microcosm of the theological and intellectual turbulence within what is often mistakenly seen as a monolithic ` religious right ' in America '' .",
r"Princeton Review , in its 2007 rankings , called JMU one of `` America 's Best Value Colleges '' .",])

dictVerbToSentences["call"].append([r"He quickly called on Ghana and Tunisia and Morocco and Guinea and Mali , which dispatched troops within hours .",
r"At the order of the Dowager Electress , the Hanoverian agents , supported by the Whig leaders , demanded that a writ of summons be issued which would call the Duke to England to sit in Parliament , thus further insuring the Succession by establishing a Hanoverian Prince in England before the Queen 's death .",
r"Five years were spent with the Cologne Opera , after which he was called to Prague by Alexander von Zemlinsky , teacher of Arnold Schonberg and Erich Korngold .",])

dictVerbToSentences["call"].append([r"On July 18th , 2014 , it was announced that Erskine College and Seminary called Dr. Paul Kooistra , an ordained minister in the Presbyterian Church in America , as their president .",])

#----------------- conduct -----------------
dictVerbToSentences["conduct"] = []

dictVerbToSentences["conduct"].append([r"I heard the Classical Symphony for the first time when Koussevitzky conducted it in Paris in 1927 .",
r"During his five-month visit abroad , Jorda recently conducted the Orchestre Philharmonique De Bordeau in France , and the Santa Cecilia Orchestra in Rome .",
r"The gala opening of the Stevens Center featured the school 's symphony orchestra conducted by Leonard Bernstein , with Isaac Stern as soloist and Gregory Peck as the Master of Ceremonies .",])

dictVerbToSentences["conduct"].append([r"The TAKS results follow the results of an independent evaluation by Rockman et al. , an independent research and evaluation firm based in San Francisco that was conducted in Grand Prairie ISD in early 2010 .",
r"Significant forward motion was accomplished by the first National Holistic Education Conference that was conducted with The University of California , San Diego in July 1979 , that included 31 workshops .",
r"In 1997 , The National Institute of Justice -LRB- NIJ -RRB- and the United States Bureau of Justice Statistics -LRB- BJS -RRB- conducted the National College Women Sexual Victimization -LRB- NCWSV -RRB- survey .",])

#----------------- enter -----------------
dictVerbToSentences["enter"] = []

dictVerbToSentences["enter"].append([r"The following morning , as John entered the Place Molard on his way to visit a sick refugee , he had a premonition of danger .",])

dictVerbToSentences["enter"].append([r"In November 2006 , SCC entered into a unique partnership with the Eastern Band of Cherokee Indians that created the Oconaluftee Institute for Cultural Arts -LRB- OICA -RRB- in Cherokee and North Carolina .",
r"NTCC and Texas A & M University at College Station have entered into an articulation agreement to provide a seamless transition for students who completed the Associate of Science Degree in Biomedical Science at NTCC to a Bachelor of Science Degree in Biomedical Science at Texas A & M. NTCC students must complete the A.S. degree with a 3.6 GPA , with no grades below `` B '' in science and math .",
r"Shortly thereafter , Spelman entered into an `` agreement of affiliation '' with nearby Morehouse College and Atlanta University by chartering the Atlanta University Center in 1929 .",])

#----------------- follow -----------------
dictVerbToSentences["follow"] = []

dictVerbToSentences["follow"].append([r"Phil followed Eddie into the office and shut the door .",
r"By 1894 , Dewey had joined Tufts , with whom he would later write Ethics -LRB- 1908 -RRB- , at the recently founded University of Chicago and invited Mead and Angell to follow him , the four men forming the basis of the so-called `` Chicago group '' of psychology .",])

dictVerbToSentences["follow"].append([r"It is followed by Cain Street and Piedmont Avenue and NE ; ;",
r"The largest college , in terms of enrollment , is the Carnegie Institute of Technology with 400 students in the class of 2017 , followed by the Dietrich College of Humanities & Social Sciences with 265 , and the College of Fine Arts with 260 .",
r"The first and best known of these schools is St. John 's College in Annapolis and Santa Fe -LRB- program established in 1937 -RRB- ; it was followed by Shimer College in Chicago , The Integral Program at Saint Mary 's College of California -LRB- 1955 -RRB- , The College of Saint Mary Magdalen in Warner , New Hampshire , and Thomas Aquinas College in Santa Paula and California .",
r"She and Bodichon founded the first higher educational institution for women , with five students , which became Girton College , Cambridge in 1873 , followed by Lady Margaret Hall at Oxford in 1879 .",
r"The first Liberal Arts degree program in Sweden was established at Gothenburg University in 2011 , followed by a Liberal Arts Bachelor Programme at Uppsala University 's Campus Gotland in the autumn of 2013 .",])

#----------------- give -----------------
dictVerbToSentences["give"] = []

dictVerbToSentences["give"].append([r"All belong to the collection being given to Wilmington over a period of years by Mrs. Sloan , who has cherished such revelatory items ever since she first studied with Sloan at the Art Students League , New York , in the 1920 's .",
r"By her eighteenth birthday her bent for writing was so evident that Papa and Mamma gave her a Life Of Dickens as a spur to her aspiration .",
r"The J. Hal Daughdrill Award is given to the `` Most Valuable Player '' of the Lynx football team .",
r"Among many alumni who have followed in George Washington 's footsteps by donating generously , Rupert Johnson , Jr. , a 1962 graduate who is vice chairman of the $ 600-billion Franklin Templeton investment management firm , gave $ 100 million to Washington and Lee in June 2007 , establishing a merit-based financial aid and curriculum enrichment program .",
r"In 2011 the Khalifa Bin Zayed Al Nahyan Foundation gave $ 150 million to MD Anderson .",])

dictVerbToSentences["give"].append([r"In 2012 , the British Academy invited AuthorAID at INASP to talk about mentoring at the Career Development Workshop for Early Career Researchers in West Africa , and a talk on mentoring was also given at the 11th General Assembly of the European Association of Science Editors .",
r"Franklin Delano Roosevelt gave a summer commencement address at the University of Georgia in 1938 .",
r"Overall , six U.S. presidents and three foreign presidents have given Landon Lectures at K-State since the series was inaugurated in 1966 .",])

#----------------- have -----------------
dictVerbToSentences["have"] = []

dictVerbToSentences["have"].append([r"LSU also has an active Society of American Archivists student chapter .",
r"See also : Lombardi Scholars Program and Reitz Scholars ProgramThe University of Florida has a nationally recognized honors program .",
r"Academic profile -LRB- edit -RRB- NCTC has a Lifelong Learning Division that recently held the first-ever Weld-Off with over 155 registrations and 42 participants .",
r"The university has two National Science Foundation Engineering Research Centers : the Integrated Media Systems Center and the Center for Biomimetic Microelectronic Systems .",])

dictVerbToSentences["have"].append([r"The Netherlands and Germany and Denmark and Belgium and France have between 30 and 10 % of their researchers coming from foreign countries .",
r"Brazil and Spain and Japan and Italy and India have less than 10 % of their researchers coming from foreign countries .",
r"According to historian Joel Ricks in 1938 , '' Provo had received the Insane Asylum , Salt Lake City had the University and Capitol , and the majority of the legislature felt that the new institutions should be given to Weber and Cache Counties . ''",
r"Canada and Australia , the United States and Sweden and the United Kingdom have between 50 and 30 % of their researchers coming from foreign countries .",])

#----------------- head -----------------
dictVerbToSentences["head"] = []

dictVerbToSentences["head"].append([r"By rough estimate her Committee , headed by Henry Francis Du Pont , contains three times as many Republicans as Democrats .",
r"A senate subcommittee headed by Sen. Jackson of Washington has been going over the State Department and has reached some predictable conclusions .",
r"The Museum of Art was founded in 1936 and originally headed by Oscar Jacobson , the director of the School of Art at the time .",
r"The University of Arizona Honors College is in affiliation with the University of Arizona and is headed by Dean Dr. Patricia MacCorquodale and Associate Dean Dr. Laura Berry .",
r"The Andrew and Erna Viterbi School of Engineering is headed by Dean Yannis Yortsos .",])

dictVerbToSentences["head"].append([r"On a bitterly cold day in January , 1895 , accompanied only by Neal Brown as his deputy , Tilghman left the township of Guthrie and headed for Rock Fort and Dunn 's ranch .",
r"The station wagon and the old Plymouth headed east toward Jarrodsville .",])

#----------------- introduce -----------------
dictVerbToSentences["introduce"] = []

dictVerbToSentences["introduce"].append([r"So right away Claude introduced Henri to his famous `` moon '' bench and proceeded to teach him his first Push-Pull Super-Set consisting of the wide-grip Straight-Arm Pullover -LRB- the `` pull '' part of the Push-Pull Super-Set -RRB- which dramatically widens the ribcage and strongly affects the muscles of the upper back and chest and the collar-to-collar Bench Press which specifically works on the chest to build those wide , Reeves-type `` gladiator '' pecs , while stimulating the upper lats and frontal deltoids .",
r"But court adjourned after he testified he introduced James White and Jeremiah Hope Pullings , two of the defendants , and also introduced Pullings to Jessy Maroy , a man mentioned in the indictment but not indicted .",
r"My cousin Alma , at whose home I was staying during the convention , introduced me to a group of young people from Rhode Island .",])

dictVerbToSentences["introduce"].append([r"Still another approach to the changeable letter type of sign is a modular unit introduced by Merritt Products , Azusa and Calif. .",
r"In 1946 , Ohio Wesleyan introduced a new `` Centennial Curriculum '' , which enacted seven distribution requirements across the sciences and humanities ; the new requirement for a foreign language course was added to the existing humanities requirement .",
r"The first Real Time Research session that was introduced at the conference by Eric Zimmerman , Constance Steinkuehler , and Kurt Squire .",
r"In response , the organization drafted model legislation , called the Academic Bill of Rights , which has been introduced in several state legislatures and the U.S. House of Representatives .",])

#----------------- know -----------------
dictVerbToSentences["know"] = []

dictVerbToSentences["know"].append([r"Both Baker and Fosdick knew that a substitute was necessary , that a verboten approach was not the real answer .",
r"The Serge Prokofieff whom we knew in the United States of America was gay , witty , mercurial , full of pranks and bonheur , and very capable as a professional musician .",
r"Alexander knew Spencer too well to think him naive or thick-skulled .",
r"The fact is that the Italians , French and British know that they have no defense against nuclear bombs .",])

dictVerbToSentences["know"].append([r"Until 2008 , Glynd University was known as the North-East Wales Institute of Higher Education -LRB- NEWI -RRB- .",
r"The University was first officially known as Western State Normal School , and originally offered a 2-year training program .",
r"Texas A&M - Corpus Christi was formerly known at various times by one of the following three names : Corpus Christi State University , Texas A&I University at Corpus Christi , and the University of Corpus Christi -LRB- a Baptist university founded in 1947 -RRB- before joining the Texas A&M University System in 1989 .",
r"University of North Carolina at PembrokeFrom Wikipedia , the free encyclopedia.uncp.edu The University of North Carolina at Pembroke -LRB- UNCP -RRB- , also known as UNC Pembroke , is a public , co-educational , historically American Indian liberal arts university in the town of Pembroke in Robeson County and North Carolina and United States .",
r"Other buildings on campus include : Malcolm A. Love Library and the InfoDomeThe campus library , now known as the Malcolm A. Love Library , acquired its 100,000 th book on May 21 , 1944 .",
r"At the same time , the college expanded its curriculum through the addition of the College of Liberal Arts , now known as the College of Arts and Sciences .",
r"El Paso -LRB- `` the Pass '' -RRB- Hall is the interior lower level of a bridge that connects the east and west sides of the campus , which are separated by a shallow but picturesque creek originally known as Jackson Branch .",
r"When the school was first established , the Tempe Normal School teams were simply known as the Normals .",])

#----------------- lead -----------------
dictVerbToSentences["lead"] = []

dictVerbToSentences["lead"].append([r"With the most casual and relaxed manner in the world , Dolores led Anthea to the bedroom .",
r"If Wilhelm Reich is the Moses who has led them out of the Egypt of sexual slavery , Dylan Thomas is the poet who offers them the Dionysian dialectic of justification for their indulgence in liquor , marijuana , sex , and jazz .",
r"Ruth himself , still owning his farm in Massachusetts and an interest in the Massachusetts cigar business that printed his round boyish face on the wrappers , had led the parade down from Fenway Park , followed by pitchers Carl Mays , Leslie `` Joe '' Bush , Waite Hoyt , Herb Pennock , and Sam Jones , catcher Wally Schang , third baseman Joe Dugan -LRB- who completed the `` playboy trio '' of Ruth , Dugan , and Hoyt -RRB- , and shortstop Everett Scott .",])

dictVerbToSentences["lead"].append([r"according to many critics , in fact , the South has led the North in literature since the Civil War , both quantitatively and qualitatively .",
r"In the popular sport of soccer UCLA leads USC in the all-time series 13 , yet USC no longer competes in men 's NCAA Div 1 soccer .",
r"Worldwide -LRB- edit -RRB- Two professors , a graduate , and an undergraduate student at the TAMUQ branch campusTexas A&M has participated in over 500 research projects in over 80 countries and leads the Southwestern United States in annual research expenditures .",])

dictVerbToSentences["lead"].append([r"Started in the fall of 2010 , the Entrepreneurship and Innovation Program is led by Director Jay A. Smith .",
r"One of the most generous contributors was De Forenede Teglv i Aarhus -LRB- `` The United Tileworks of Aarhus '' -RRB- led by director K. Nymark .",
r"Founded in the fall of 2011 , Integrated Life Sciences is currently led by Director Dr. Todd J. Cooke .",
r"Cooper , a two-time WNBA MVP , led the Lady Panthers to the school 's first ever SWAC title and NCAA Tournament berth in her second season as coach .",
r"David Bassore was announced head coach in 2005 and led the Eagles to a 6-5 record and a district championship .",
r"From 2010-2012 , Wagner Men 's Basketball was coached by Dan Hurley , who led Wagner to a 38 -LRB- 24 NEC -RRB- record in his two seasons before taking the Head Coaching Job at the University of Rhode Island .",
r"RHA is led by an Executive Board and Senate with student representatives from each residence hall hall .",
r"In 2002 , Floridians led by U.S. Senator Bob Graham passed an amendment to the Florida Constitution establishing a new statewide governing body , the Florida Board of Governors .",
r"A Campaign Steering Committee of alumni and friends is led by co-chairs Patricia V. Reser , James H. Rudd and Patrick F. Stone .",])

#----------------- live -----------------
dictVerbToSentences["live"] = []

dictVerbToSentences["live"].append([r"Little by little , during the week , Chris and I discovered the crazy unbelievable way Nadine and Wally had lived .",])

dictVerbToSentences["live"].append([r"Both Red McIver and Handley Walker lived nearby , almost as near as I do .",
r"Mr. and Mrs. Robert Moulton now live on Wilshire and the Franklin Moultons on S. Windsor Blvd. .",
r"The Mayor declined in two interviews with reporters yesterday to confirm or deny the reports that he had decided to run and wanted Mr. Screvane , who lives in Queens , to replace Abe Stark , the incumbent , as the candidate for President of the City Council and Mr. Beame , who lives in Brooklyn , to replace Mr. Gerosa as the candidate for Controller .",
r"The Beadles formerly lived in Lake Forest .",
r"In talks with Mr. Buckley last week in Washington , the Mayor apparently received the Bronx leader 's assent to dropping Controller Lawrence E. Gerosa , who lives in the Bronx , from this year 's ticket .",
r"Hengesbach has been living in Grand Ledge since his house and barn were burned down after his release in 1958 .",
r"After her father 's death , Lucy and her youngest sister lived for a few years with Winslow in Washington and D.C. .",
r"Many years later I went to see S.K. in England , where he was living at Whiteleaf , near Aylesbury , and he showed me beside his cottage there the remains of the road on which Boadicea is supposed to have traveled .",
r"Billy Koch , who had once worked for Wright as a chauffeur , gave a deposition for Miriam 's use that he had seen Olgivanna living at Taliesin .",
r"Now a family man with three children , Fiedler lives in a quiet residential area near the Lockheed plant at Sunnyvale .",
r"Handley lived further on , at Pigeon Cove .",
r"Billy decided to set an example by arresting one of the ranchers , named Ed Dunn , who lived at Rock Fort .",])

dictVerbToSentences["live"].append([r"`` The Moral Creed '' and `` The Will To Risk '' live happily together , if we do not examine where the line is to be drawn .",])

#----------------- make -----------------
dictVerbToSentences["make"] = []

dictVerbToSentences["make"].append([r"The New Testament offered to the public today is the first result of the work of a joint committee made up of representatives of the Church of England , Church of Scotland , Methodist Church , Congregational Union , Baptist Union , Presbyterian Church of England , Churches in Wales , Churches in Ireland , Society of Friends , British and Foreign Bible Society and National Society of Scotland .",
r"As of 2007 , the Board is made up of three Republicans and five Democrats .",
r"Debates Selection Committee -LRB- to operate debating selections -RRB- Made up of the Director of Debating , the President , the Treasurer , the Debates Training Secretary and the Debates Competitions Secretary , the DSC decides which members of the competitive debating squads will go to which competitions and who will be Durham 's adjudicators .",
r"Governance -LRB- edit -RRB- Northeast Mississippi Community is governed locally by a Board of Trustees which is made up of fifteen members members from Prentiss and two each from Alcorn and Tippah and Tishomingo , and Union counties with one member elected at-large by the Board itself .",
r"The college has a music program and supports the Austin College A Cappella Choir along with the Sherman Symphony Orchestra made up of students and local musicians , and assorted smaller musical ensembles .",])

dictVerbToSentences["make"].append([r"National Pan-Hellenic Council is made up of 9 organizations , 5 Fraternities and 4 Sororities , that were founded on Historically Black College and Universities -LRB- HBCU 's -RRB- .",
r"Lumbee Hall , the Dial Humanities building , the Sampson building , Auxiliary building , and the Jones Athletic Center make up most of the north end of campus .",])

#----------------- move -----------------
dictVerbToSentences["move"] = []

dictVerbToSentences["move"].append([r"They do not move to Chicago , they move to the South Side ; ;",
r"but I liked to think of him at ninety swimming and working at Key West long after Hemingway had moved to Cuba .",
r"In 1838 , a devastating fire gutted their small shop and soon thereafter David Brown moved west to Illinois , settling on a land grant in his declining years .",
r"Gorton then moved to Providence and soon put the town in a turmoil .",
r"Gorton and his family moved to Plymouth .",
r"Judge and Mrs. Julian Hazard are now at Laguna Beach , while the Frank Wangemans have moved from Beverly Hills to New York , where he is general manager of the Waldorf-Astoria Hotel .",
r"The item said Mr. and Mrs. Black had moved to Jackson , his home town , so the lovely Lisa had been with him a year ago .",
r"In the fall of 1913 , H.K. Taylor moved from Missouri where he was president of the Northwest State Teachers ' College to set up another military academy called Arlington Training School .",
r"Thomas Martin , son of a Methodist minister , was born in 1799 and moved to Pulaski Tennessee , as a young man .",
r"In 1908 Rev. Kelley and his bride moved to Orlinda and Tennessee to take the pastorate at Orlinda Baptist Church .",])

dictVerbToSentences["move"].append([r"The second half of the 20th century saw Washington and Lee move from being an all-men 's college to a co-ed university .",])

#----------------- operate -----------------
dictVerbToSentences["operate"] = []

dictVerbToSentences["operate"].append([r"The college also operates the SAU Tech Career Academy , the Ouachita County Adult Education Center , the Arkansas Fire Training Academy , and the Arkansas Environmental Training Academy .",
r"The university also operates the Fort Worth Education Center and the UTA Research Institute , with campuses at the Fort Worth ITC and River Bend Park .",
r"The Software Engineering Institute -LRB- SEI -RRB- is a federally funded research and development center sponsored by the U.S. Department of Defense and operated by Carnegie Mellon University , with offices in Pittsburgh and Pennsylvania and USA ; Arlington and Virginia , and Frankfurt and Germany .",
r"Beginning in Spring of 2004 , Cedar Valley College began operating the Cedar Valley College Center at Cedar Hill .",
r"In addition , the Penn State College of Communications operates ComRadio .",
r"The university also operates the 18-hole Kent State Golf Course and Centennial Research Park just east of campus in Franklin Township and the 219-acre -LRB- 0.9 -RRB- Kent State University Airport in Stow .",])

dictVerbToSentences["operate"].append([r"There are 51 scientific and scholarly associations , societies and unions affiliated with the SAS , which operate in accordance with the Law on Civic Associations .",
r"'' Kenyon , Sewanee , and Hudson operated in an `` Anglo-Protestant New Critical chill '' ; ;",])

#----------------- place -----------------
dictVerbToSentences["place"] = []

dictVerbToSentences["place"].append([r"Last year Susan also placed 3rd in the Finals at Westminster .",
r"CMU placed 51st among the top universities in the world in the current Academic Ranking of World Universities -LRB- ARWU -RRB- .",
r"College of Health ProfessionsFairmount College of Liberal Arts and SciencesWichita State is placed among Tier 2 National Universities in the United States .",])

dictVerbToSentences["place"].append([r"From the records we keep , Susan is the only Junior who has placed in the Junior Classes in both United States and Canada .",
r"In 1958 , Wilmington College was placed under the Community College Act of North Carolina , passing control from the New Hanover County Board of Education to a board of trustees as a state-supported college under the supervision of the North Carolina Board of Higher Education .",
r"The National Park Service placed Pinkerton Hall , the oldest building on campus , on the National Register of Historic Places on November 20 , 1974 .",])

#----------------- play -----------------
dictVerbToSentences["play"] = []

dictVerbToSentences["play"].append([r"Louis Seigner , who formerly played the deluded benefactor opposite Ledoux , is the Tartuffe of the present production , which he himself directed .",
r"Joan Fagan , a fiery redhead who can impress you that she has a temper whether she really has one or not , plays Ellen , and sings the role very well , too .",
r"Then there are a pair of old biddies played by Grace Carney and Sibly Bowan who may be right off the shelf of stock Irish characters , but they put such a combination of good will and malevolence into their parts that they 're quite entertaining .",])

dictVerbToSentences["play"].append([r"SMU will play the Owls at Rice Stadium in Houston in a night game Saturday , Oct. 21 .",
r"The Prairie View Bowl was played in Texas between 1928 and 1962 .",
r"Former Dragon Brian Wuest now plays for the University of Nebraska at Kearney Lopers .",
r"Notable football players that have achieved success in the National Football League -LRB- NFL -RRB- are National Football Hall of Fame Inductee Kenny Houston , who played for the Houston Oilers and Washington Redskins and Otis Taylor , who won a World Championship with the Kansas City Chiefs in 1969 .",
r"The Cougars play in an extremely talented and competitive JUCO Conference .",
r"11 Wildcats have played in the NFL .",])

dictVerbToSentences["play"].append([r"In recent years Anna Xydis has played with the New York Philharmonic and at Lewisohn Stadium , but her program last night at Town Hall was the Greek-born pianist 's first New York recital since 1948 .",
r"Music lovers who are not familiar with this literature may hear an excellent example , played for RCA by Emil Gilels .",])

#----------------- run -----------------
dictVerbToSentences["run"] = []

dictVerbToSentences["run"].append([r"The Boulevard De La Madeleine , the Boulevard Malesherbes , and the Rue Royale ran to it with graceful flattery , bearing tidings of the Age of Reason .",
r"Duclos ran toward Desprez with fists raised .",
r"The Little Brown Jug , a harness race , is run during the Delaware County Fair in September .",])

dictVerbToSentences["run"].append([r"During Dulles 's first two years in office , while Republicans ran the Senate , the Department was at the mercy of men who had thirsted for its blood since 1945 .",
r"The International Center for Lightning Research and Testing -LRB- ICLRT -RRB- are run by the University of Florida at the Camp Blanding Florida Army National Guard Base .",
r"USC ran the Chaffey College of Agriculture until financial troubles closed the school in 1901 .",
r"In 2001 the Sapling Foundation , run by entrepreneur Chris Anderson , acquired TED .",])

#----------------- serve -----------------
dictVerbToSentences["serve"] = []

dictVerbToSentences["serve"].append([r"Tibet has historically served China as a buffer state .",
r"So instead of being tests of the South 's loyalty , the Spanish War , the two World Wars , and the Korean War all served to overcome old grievances and cement reunion .",])

dictVerbToSentences["serve"].append([r"The 1946 town meeting voted to have the Selectmen appoint a committee to investigate and report on the feasibility of some system of sewage disposal and a disposal plant to serve Manchester Center , Depot , and Way 's Lane .",
r"RTS has largely served the Presbyterian Church in America since that denomination 's founding in 1973 .",
r"HCS Blue -LRB- # 00a7cf -RRB- and Black -LRB- # 00000 -RRB- Other information : www.horrycountyschools.netH orry County Schools -LRB- HCS -RRB- is a public school district serving Horry County and South Carolina and is the third-largest school district in South Carolina .",
r"Sargeant Reynolds Community College -LRB- Reynolds -RRB- is a community college serving not only Richmond and Virginia , but Goochland County and Hanover County and Henrico County and Louisa County and Powhatan County as well .",])

dictVerbToSentences["serve"].append([r"Hester College , named for Cleo Gillis Hester , who served Murray State University from 1927 , as registrar .",
r"Previously , Allison served as provost and vice president at Governor 's State University in Illnois where he was also a professor of English .",
r"Immediately before that , Dr. Howard served for fifteen years as a Vice President at the University of North Alabama .",
r"After the dissolution of the system , Alvin Duke Chandler served as the coordinator for Christopher Newport College and Richard Bland College ; however , he resigned this position after only four months .",
r"Gougenheim , R Michea , Paul Rivenc , and Aur Sauvageot served as researchers for the project .",
r"Hutchins served as President of the University of Chicago until 1945 , and as the University 's Chancellor until 1951 .",])

#----------------- succeed -----------------
dictVerbToSentences["succeed"] = []

dictVerbToSentences["succeed"].append([r"Pfaff succeeds Martin Burke , who resigned .",
r"Mr. Oakes succeeds Charles Merz , editor since 1938 , who now becomes editor emeritus .",
r"Dr. Clark will succeed Dr. J. R. McLemore , who will retire at the close of the present school term .",
r"In 1927 he succeeded Zemlinsky as opera director of the German Theater at Prague .",
r"After the school had changed locations several times , Bishop Haven , who succeeded Bishop Clark , was instrumental in acquiring 450 acres -LRB- 1.8 -RRB- in South Atlanta , where in 1880 the school conferred its first degree .",
r"Governor Steve Beshear , who succeeded Fletcher in 2007 , has stated that the state does not plan to appeal this decision .",
r"In 1943 , Dr. Jennings B. Sanders succeeded Jones as president .",])

dictVerbToSentences["succeed"].append([r"A burlesque paean entitled : `` Hark The Herald Tribune , Times , And All The Other Angels Sing '' brilliantly succeeds in exaggerating even motion-picture ballyhooey .",
r"According to the Food And Drug Administration -LRB- FDA -RRB- , `` Doctor '' Ghadiali , Dr. Albert Abrams and his clique , and Dr. Wilhelm Reich , to name three notorious device quacks , succeeded , respectively , in distributing 10,000 , 5000 , and 2000 fake health machines .",
r"The inference has been too widely accepted that because the Communists have succeeded in building barricades across Berlin the free world must acquiesce in dismemberment of that living city .",])

#----------------- take -----------------
dictVerbToSentences["take"] = []

dictVerbToSentences["take"].append([r"A weapons carrier took Greg , Todman , Belton , Banjo Ferguson , and Walters and the others the two miles from the bivouac area to the strip .",
r"Max , in a fit of despair , takes Alicia and runs off for two marvelous weeks in Burbank -LRB- Fink calls it `` the most wonderful and lovely fourteen days in my whole life '' -RRB- , at the end of which Alicia tragically contracts Parkinson 's disease and dies .",
r"One afternoon during a cold , powdery snowstorm , Fogg took off for Concord from the St. John field .",
r"Her father 's attention would be on the road ahead and it would n't deviate an inch until he crossed the bridge at the Falls and took the River Road to LaSalle and , finally , turned in at their own driveway at 387 Heather Heights .",
r"In his first season , Rodriguez took the Wildcats to the 2012 New Mexico Bowl , where they defeated the University of Nevada Wolfpack .",])

dictVerbToSentences["take"].append([r"In the midst of this gloom , at 10:05 P.M. on September 2 , Slocum 's telegram to Stanton , `` General Sherman has taken Atlanta '' , shattered the talk of a negotiated peace and boosted Lincoln into the White House .",
r"The Federal forces had taken Parkersburg and Grafton from the Rebels and were moving to take all the mountains .",])

dictVerbToSentences["take"].append([r"Harold , with brothers Frank , Joe and William , took over at the death of their father , Harry M. Stevens , who put a few dollars into a baseball program , introduced the `` hot dog '' and paved the way for creation of a catering empire .",
r"Olivetti took over Underwood , the U.S. typewriter maker , in late 1959 .",])

#######
sentences = []
for verb in dictVerbToSentences.keys():
    for sents in dictVerbToSentences[verb]:
        for sent in sents:
            sentences.append(sent)
random.shuffle(sentences)
pickle.dump( sentences, open('ambigiousSentences.p', 'wb'))


