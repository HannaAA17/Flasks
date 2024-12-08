from application import app, db
from application.models import Member, Order, Course
from datetime import date

with app.app_context():
    # # create
    # hanna = Member(
    #     username='hanna', password='secret',
    #     email='hanna@gmail.com', join_date=date.today()
    # )
    # 
    # db.session.add(hanna)
    # db.session.commit()

    # # edit
    # hanna.password = 'supersecretpassword'
    # db.session.commit()

    # # delete
    # db.session.delete(hanna)
    # db.session.commit()
    
    # # query
    # for m in Member.query.all():
    #     print(repr(m))
    
    # using filter_by
    # ant = Member.query.filter_by(username='andy').first()
    # print(ant)

    # # using filter
    # ant = Member.query.filter(Member.username=='andy').first()
    # print(ant)

    # # using not equal
    # q = Member.query.filter(Member.username != 'andy')
    # print(q.all())
    
    # # using like
    # q = Member.query.filter(Member.username.like('%dy'))
    # print(q.all())

    # # using in
    # q = Member.query.filter(Member.username.in_(['andy']))
    # print(q.all())
    
    # # using not in
    # q = Member.query.filter(~Member.username.in_(['andy']))
    # print(q.all())

    # # query for Null and not Null
    # q = Member.query.filter(Member.email == None)
    # print(q.all())
    # 
    # q = Member.query.filter(Member.email != None)
    # print(q.all())

    # # using and
    # q = Member.query.filter(Member.email!=None).filter(Member.username=='andy')
    # print(q.all())
    # q = Member.query.filter(Member.email!=None, Member.username=='andy')
    # print(q.all())
    # q = Member.query.filter(db.and_(Member.email!=None, Member.username=='andy'))
    # print(q.all())
    
    # # using or
    # q = Member.query.filter(db.or_(Member.email==None, Member.username=='andy'))
    # print(q.all())

    # # using order_by
    # q = Member.query.order_by(Member.username)
    # print(q.all())

    # # using limit
    # q = Member.query.limit(2)
    # print(q.all())
    
    # # using offset ( skip the first 2 )
    # q = Member.query.offset(2)
    # print(q.all())

    # # using count
    # q = Member.query
    # print(q.count())

    # # creating an Order with a User object as an argument
    # anthony = Member.query.filter(Member.username=='anthony').first()
    # print(anthony.orders.all())
    # order = Order(price=120, member=anthony)
    # db.session.add(order)
    # db.session.commit()
    # print(anthony.orders.all())
    
    # # testing many to many
    # anthony = Member.query.filter(Member.username=='anthony').first()
    # andy = Member.query.filter(Member.username=='andy').first()
    # 
    # cr1 = Course(name='java course')
    # db.session.add(cr1)
    # db.session.commit()
    # 
    # cr1.members.append(anthony)
    # cr1.members.append(andy)
    # db.session.commit()
    # 
    # cr1 = Course.query.filter(Course.id=='3').first()    
    # print(cr1.members)
    
    
    
    '''
    # populate data
    from datetime import date
    a1 = Member(username='anthony', password='secret', join_date=date.today())
    a2 = Member(username='andy', password='secret', email='andy@gmail.com', join_date=date.today())
    a3 = Member(username='peter', password='secretpassword', email='peter@gmail.com', join_date=date.today())
    a4 = Member(username='hanna', password='supersecretpassword', email='hanna@gmail.com', join_date=date.today())
    db.session.add_all([a1, a2, a3, a4])
    db.session.commit()


    o1 = Order(price=50, member_id=1)
    o2 = Order(price=50, member_id=2)
    o3 = Order(price=50, member_id=3)
    o4 = Order(price=50, member_id=4)
    o5 = Order(price=100, member_id=1)
    o6 = Order(price=200, member_id=1)
    db.session.add_all([o1, o2, o3, o4, o5, o6])
    db.session.commit()
    '''