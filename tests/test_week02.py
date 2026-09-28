"""
Week 02 Autograder: Self-Driving Car, Foute Sensor en Routeplanner.

Test de publieke interface van de oplossing van de student:
- SelfDrivingCar: process() met remlogica
- FaultTolerantAgent: plausibiliteitscheck en interne state
- RouteAgent: utility-based greedy routeplanner

Breadth-First Search en Sliding Puzzle zijn opgeschoven naar week 3;
die tests staan in test_week03.py.

De tests controleren enkel gedrag, niet hoe het geimplementeerd is.
"""

import contextlib
import importlib
import threading

import pytest

MODULE_PATH = "exercises.week02.solution"

try:
    _mod = importlib.import_module(MODULE_PATH)
    SelfDrivingCar = _mod.SelfDrivingCar
    LidarSensorInput = _mod.LidarSensorInput
    Brake = _mod.Brake
    Nothing = _mod.Nothing
    Reading = _mod.Reading
    Correct = _mod.Correct
    FaultTolerantAgent = _mod.FaultTolerantAgent
    RouteAgent = _mod.RouteAgent
    distance = _mod.distance
except Exception as import_error:
    pytest.skip(
        f"solution.py kon niet geimporteerd worden: {import_error}",
        allow_module_level=True,
    )

WEIGHTS = {
    # Self-Driving Car
    "test_selfdriving_initial": 1,
    "test_selfdriving_brake": 2,
    "test_selfdriving_no_brake": 1,
    # Foute Sensor
    "test_faulty_sensor_agreement": 2,
    "test_faulty_sensor_detects_failure": 3,
    "test_faulty_sensor_trusted_descent": 2,
    # Routeplanner
    "test_route_utility_negative": 1,
    "test_route_choose_next": 2,
    "test_route_plan_reaches_goal": 2,
    "test_route_no_path_none": 1,
}


@contextlib.contextmanager
def time_limit(seconds: int = 5):
    """Beperk de duur van een blok code (tegen infinite loops).

    Gebruikt threading.Timer omdat SIGALRM niet werkt op Windows.
    """
    timeout_triggered = False

    def _raise():
        nonlocal timeout_triggered
        timeout_triggered = True

    timer = threading.Timer(seconds, _raise)
    timer.start()
    try:
        yield
        if timeout_triggered:
            raise TimeoutError(f"code duurde te lang (>{seconds}s)")
    finally:
        timer.cancel()


# =============== Oefening 1: Self-Driving Car ===============


def test_selfdriving_initial():
    """Bij de eerste meting wordt er nog niet geremd."""
    car = SelfDrivingCar()
    sensor = LidarSensorInput(10)
    with time_limit():
        action = car.process(sensor)
    assert isinstance(action, Nothing), (
        "eerste meting moet Nothing teruggeven"
    )


def test_selfdriving_brake():
    """Remmen wanneer de voorligger snel dichterbij komt."""
    car = SelfDrivingCar()
    sensor = LidarSensorInput(10)
    # eerste meting (initialisatie)
    car.process(sensor)

    # voorligger komt snel dichter: 10m -> 4m in 1 stap
    sensor.DistanceTo = 4
    with time_limit():
        action = car.process(sensor)
    assert isinstance(action, Brake), (
        "moet remmen bij tijd tot botsing < 5s"
    )


def test_selfdriving_no_brake():
    """Niet remmen wanneer de voorligger veilig veraf blijft."""
    car = SelfDrivingCar()
    sensor = LidarSensorInput(10)
    car.process(sensor)

    # voorligger rijdt weg: 10m -> 20m
    sensor.DistanceTo = 20
    with time_limit():
        action = car.process(sensor)
    assert isinstance(action, Brake) is False, (
        "mag niet remmen bij veilige afstand"
    )

# =============== Oefening 2: Foute Sensor ===============


def _agent_met_startmeting():
    """Agent met een geldige beginmeting (zowel a als b = 1000)."""
    agent = FaultTolerantAgent()
    agent.process(Reading(1000, 1000))
    return agent


def test_faulty_sensor_agreement():
    """Sensoren in overeenstemming: gemiddelde gebruiken, geen correctie."""
    agent = FaultTolerantAgent()
    with time_limit():
        actie = agent.process(Reading(1000, 1010))
    assert isinstance(actie, Nothing), (
        "in overeenstemming -> gemiddelde gebruiken, geen correctie"
    )


def test_faulty_sensor_detects_failure():
    """Sensor B valt weg: agent vertrouwt A op basis van vorige waarde."""
    agent = _agent_met_startmeting()
    # discrepantie: B meet onzin (400 ipv ~1000)
    with time_limit():
        actie = agent.process(Reading(1000, 400))
    assert isinstance(actie, Nothing), (
        "betrouwbare meting is stabiel -> geen correctie"
    )
    # verdachte sensor moet in de interne state staan
    verdacht = getattr(agent, "suspected_sensor", None)
    assert verdacht in ("b", "B"), (
        "sensor b moet als verdacht opgeslagen worden"
    )


def test_faulty_sensor_trusted_descent():
    """Zelfs met een sturende sensor B ziet de agent de daling via A."""
    agent = _agent_met_startmeting()
    agent.process(Reading(1000, 400))  # B gaat stuk
    with time_limit():
        actie = agent.process(Reading(980, 380))
    assert isinstance(actie, Correct), (
        "betrouwbare hoogtemeter daalt > 10 -> correctie aanvragen"
    )


# =============== Oefening 3: Routeplanner ===============


def test_route_utility_negative():
    """Utility is de negatieve afstand."""
    with time_limit():
        u = RouteAgent().utility("Antwerpen", "Brussel")
    assert u == -45.0, f"verwacht -45.0, kreeg {u}"


def test_route_choose_next():
    """Greedy kiest de dichtstbijzijnde niet-bezochte buur."""
    agent = RouteAgent()
    with time_limit():
        volgende = agent.choose_next("Antwerpen", {"Antwerpen"})
    assert volgende == "Brussel", (
        f"verwacht Brussel (45 < 60), kreeg {volgende}"
    )
    with time_limit():
        none = agent.choose_next("Antwerpen", {"Antwerpen", "Brussel", "Gent"})
    assert none is None, "geen buren meer -> None"


def test_route_plan_reaches_goal():
    """De greedy route komt aan in Parijs."""
    agent = RouteAgent()
    with time_limit():
        route = agent.plan_route("Antwerpen", "Parijs")
    assert route[0] == "Antwerpen", "route begint in Antwerpen"
    assert route[-1] == "Parijs", "route eindigt in Parijs"
    # greedy pad is Antwerpen-Brussel-Gent-Doornik-Reims-Parijs (440 km)
    totaal = sum(distance(a, b) for a, b in zip(route, route[1:]))
    assert totaal == 440.0, (
        f"verwacht 440 km via greedy keuzes, kreeg {totaal}"
    )


def test_route_no_path_none():
    """Vastgelopen (geen buren meer) geeft geen oneindige loop."""
    agent = RouteAgent()
    with time_limit():
        route = agent.plan_route("Parijs", "Antwerpen")
    assert route == ["Parijs"], "geen pad vanaf Parijs: route blijft bij start"

