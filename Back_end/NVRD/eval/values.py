from eval.models import *


def add_one_panel(year_code):
    largest = Panel.objects.filter(
        year_code=year_code).order_by('panel_id').last()
    if not largest:
        return str(1).zfill(10)
    return str(int(largest.panel_id) + 1).zfill(10)


def add_one_team(year_code):
    largest = Team.objects.filter(
        year_code=year_code).order_by('team_id').last()
    if not largest:
        return str(1).zfill(10)
    return str(int(largest.team_id) + 1).zfill(10)


d = Department(dept="Computer Science")
d.save()
p = Panel(year_code="PN_20", panel_id=add_one_panel(
    "PN_20"), panel_name="AAAA")
p.save()
Panel(year_code="PN_20", panel_id=add_one_panel("PN_20"), panel_name="BBBB")
p.save()
f = Faculty(fac_id="7474", dept=Department.objects.filter(dept="Computer Science").first(),
            email="abc@gmail.com", phone="+911234567890", name="Raghavan")
f.save()
t = Team(year_code="UE_20", team_id=add_one_team(
    "UE_20"), guide=Faculty.objects.get(fac_id="7474"))
t.save()
s = Student(srn="PES1201801947", name="Rakshith", email="7r7@gmail.com", phone="+911324354657", team=Team.objects.filter(
    year_code="UE_20", team_id="0000000001").first(), dept=Department.objects.filter(dept="Computer Science").first())
s.save()
s = Student(srn="PES1201801957", name="shith", email="7r7@gmail.com", phone="+911324354657", team=Team.objects.filter(
    year_code="UE_20", team_id="0000000001").first(), dept=Department.objects.filter(dept="Computer Science").first())
s.save()
s = Student(srn="PES1201801967", name="Rak", email="7r7@gmail.com", phone="+911324354657", team=Team.objects.filter(
    year_code="UE_20", team_id="0000000001").first(), dept=Department.objects.filter(dept="Computer Science").first())
s.save()
s = Student(srn="PES1201801977", name="Ragsit", email="7r7@gmail.com", phone="+911324354657", team=Team.objects.filter(
    year_code="UE_20", team_id="0000000001").first(), dept=Department.objects.filter(dept="Computer Science").first())
s.save()
s = Student(srn="PES1201801947", name="Rakshith", email="7r7@gmail.com",
            phone="+911324354657", dept=Department.objects.filter(dept="Computer Science").first())
s.save()
f = FacultyPanel(fac_id=Faculty.objects.get(fac_id="7474"), panel_id=Panel.objects.filter(
    year_code="PN_20", panel_id="0000000001").first(), is_coordinator=True)
f.save()
