from django.db import models
from django.contrib.auth.models import User
import uuid

# Django models documentation: https://docs.djangoproject.com/en/3.1/topics/db/models/


"""
Donor
"""
class Donor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    email_address = models.EmailField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)

    address_line1 = models.CharField(max_length=50, blank=True, null=True)
    address_line2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=13, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)

    def __init__(
                self,
                first_name,
                last_name,
                email_address="",
                phone_number="",
                address_line1="",
                address_line2="",
                city="",
                state="",
                zipcode=""
                ):
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.phone_number = phone_number
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.city = city
        self.state = state
        self.zipcode = zipcode

    def __str__(self):
        return f"{self.pk} {self.first_name} {self.last_name} {self.email_address}"


"""
Donations
"""
class Donation(models.Model):
    # Donors FK
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)

    # Users FK
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    date_received = models.DateField()
    thanks_sent = models.BooleanField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __init__(
                self,
                donor=None,
                user="",
                date_received="",
                thanks_sent="",
                comments=""
                ):
        self.donor = donor
        self.user = user
        self.date_received = date_received
        self.thanks_sent = thanks_sent
        self.comments = comments

    def __str__(self):
        return f"{self.donor} {self.date_received}  {self.user}"


"""
Items
"""
class Item(models.Model):
    # Auto generated pk
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=30)

    def __init__(
                self,
                donation,
                quantity
                ):
        self.donation = donation
        self.quantity = quantity

    def __str__(self):
        return f"{self.donation} {self.quantity}"


"""
Enumerations for Item subclasses
"""


class Business(models.Model):
    # Enumeration for GiftCards table; see Giftcard
    name = models.CharField(primary_key=True, max_length=50)

    def __init__(self,name):
        self.name = name

    def __str__(self):
        return f"{self.name}"


class ClothingType(models.Model):
    # Enumeration for Clothing table; see Clothing
    name = models.CharField(primary_key=True, max_length=50)

    def __init__(self,name):
        self.name = name

    def __str__(self):
        return f"{self.name}"


class FundType(models.Model):
    # Enumeration for Funds table
    name = models.CharField(primary_key=True, max_length=50)

    def __init__(self,name):
        self.name = name

    def __str__(self):
        return f"{self.name}"


"""
Item subclasses
"""


class Clothing(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, primary_key=True)
    type = models.ForeignKey(ClothingType, on_delete=models.CASCADE)

    def __init__(
                self,
                item,
                type
                ):
        self.item = item
        self.type = type

    def __str__(self):
        return f"{self.item} {self.type}"


class Food(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50)

    def __init__(
                self,
                item,
                name
                ):
        self.item = item
        self.name = name

    def __str__(self):
        return f"{self.item} {self.name}"


class Fund(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, primary_key=True)
    type = models.ForeignKey(FundType, on_delete=models.CASCADE)
    amount = models.CharField(max_length=10)

    def __init__(
                self,
                item,
                type,
                amount
                ):
        self.item = item
        self.type = type
        self.amount = amount

    def __str__(self):
        return f"{self.item} {self.type} {self.amount}"


class GiftCard(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, primary_key=True)
    business_name = models.ForeignKey(Business, on_delete=models.CASCADE)
    amount = models.CharField(max_length=10)

    def __init__(
                self,
                item,
                business_name,
                amount
                ):
        self.item = item
        self.business_name = business_name
        self.amount = amount

    def __str__(self):
        return f"{self.item} {self.business_name} {self.amount}"


class Miscellaneous(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50)

    def __init__(
                self,
                item,
                name
                ):
        self.item = item
        self.name = name

    def __str__(self):
        return f"{self.item} {self.name}"

"""
Debug function; prints all rows in all tables
"""
def tableDebug():
    x = [Donor,Donation,Item,Fund,GiftCard,Clothing,Food,Miscellaneous,FundType,Business,ClothingType,User]
    for x1 in x:
        print(x1.objects.all())

"""
Insert a Donor into the table for Donors. Checks for uniqueness before insertion.
"""
def InsertDonor(
                first_name, # Required
                last_name,
                date_of_birth = None, # Optional
                email_address = None,
                phone_number = None,
                address_line1 = None,
                address_line2 = None,
                city = None,
                state = None,
                zipcode = None
                ):

    """
    Query Donor table for any matches; if the resulting queryset is empty,
    we can create the next one.

    If we need to add more uniqueness constraints that's fine, add them after the
    last_name argument.
    """
    donors = Donor.objects.filter(
                                first_name=first_name,
                                last_name=last_name
                                )
    if len(donors) == 0:
        # Build and save the Donor
        them = Donor(
            first_name = first_name,
            last_name = last_name,
            email_address = email_address,
            phone_number = phone_number,
            address_line1 = address_line1,
            address_line2 = address_line2,
            city = city,
            state = state,
            zipcode = zipcode
        )
        them.save()
        print(them,"created")
    else:
        print("Donor",first_name,last_name,"already exists")
    return donor

"""
Insert a Donation into the table for Donations. Also calls InsertItem(). The argument
items cannot be the empty list. It is safe to call this with the empty list, though.
The items arg should be a list of dictionaries with arguments that correspond to
InsertItem() (with the exception of the donation id, which is produced before any
calls to InsertItem()).
"""
def InsertDonation(
                    donor,
                    items,
                    date_received=None,
                    thanks_sent=None,
                    user=None,
                    comments=None
                    ):
    if len(items) == 0:
        print("Donations need an item")
    else:
        # Set up the Donation
        donation = Donation(
                            donor = donor,
                            date_received = date_received,
                            thanks_sent = thanks_sent,
                            user = user,
                            comments = comments
                            )
        donation.save()

        # Add the Items
        count = 0
        for item in items:
            try:
                InsertItem(
                            donation.id,
                            item["quantity"],
                            item["subclass"], # this name can probably be changed if needed
                            item["type"],
                            item["amount"],
                            item["name"],
                            item["fundTypeName"],
                            item["businessName"],
                            item["clothingTypeName"],
                            )
                count += 1
            except:
                print("Could not insert Item")
        print("Inserted",count,"items")

"""
Insert an Item into the table for Items and an instance of the appropriate subclass
into its corresponding table. The subclass arg is required. Other args are required
depending on the subclass you use when calling.

Usage:
    InsertItem(
                donation.donation,
                "1",
                Fund,
                amount="20",
                fundTypeName="Check",     # if you insert Fund, fundTypeName is required
                )
"""

def InsertItem(
                donation, # Required
                quantity,
                subclass,
                type="", # Optional
                amount="",
                name="",
                fundTypeName="",
                businessName="",
                clothingTypeName="",
                ):
    subclasses = [Fund,GiftCard,Clothing,Food,Miscellaneous]
    if subclass in subclasses:
        item = Item(donation,quantity)
        item.save()
        if subclass == Fund:
            fund = Fund(item,
                        FundType.objects.get(name=FundTypeName),
                        amount)
            fund.save()
        elif subclass == GiftCard:
            giftcard = GiftCard(item,
                                Business.objects.get(name=businessName),
                                amount)
            giftcard.save()
        elif subclass == Clothing:
            clothing = Clothing(item,
                                ClothingType.objects.get(name=clothingTypeName))
            clothing.save()
        elif subclass == Food:
            food = Food(item,name)
            food.save()
        elif subclass == Miscellaneous:
            misc = Miscellaneous(item,name)
            misc.save()
    else:
        print("Item subclass not recognized")
