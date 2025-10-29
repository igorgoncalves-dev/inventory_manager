from fastapi import APIRouter

machines_router = APIRouter(
    prefix="/machines", 
    tags=["machines"]
)

machines = [
    {
        "id": 1,
        "user_id": 1,
        "patrimonio": "PT-1001",
        "ram": "16GB",
        "processador": "Intel i7-11700",
        "modelo": "Dell Optiplex 7090",
        "tipo": "Desktop",
        "hd_primario": "512GB SSD",
        "hd_secundario": "1TB HDD"
    },
    {
        "id": 2,
        "user_id": 2,
        "patrimonio": "PT-1002",
        "ram": "8GB",
        "processador": "Intel i5-10400",
        "modelo": "HP ProDesk 400",
        "tipo": "Desktop",
        "hd_primario": "256GB SSD",
        "hd_secundario": "1TB HDD"
    },
    {
        "id": 3,
        "user_id": 3,
        "patrimonio": "PT-1003",
        "ram": "32GB",
        "processador": "AMD Ryzen 7 5800X",
        "modelo": "Custom Build",
        "tipo": "Desktop",
        "hd_primario": "1TB SSD",
        "hd_secundario": "2TB HDD"
    },
    {
        "id": 4,
        "user_id": 4,
        "patrimonio": "PT-1004",
        "ram": "16GB",
        "processador": "Intel i5-12600",
        "modelo": "Lenovo ThinkCentre M70q",
        "tipo": "Desktop",
        "hd_primario": "512GB SSD",
        "hd_secundario": "1TB HDD"
    },
    {
        "id": 5,
        "user_id": 5,
        "patrimonio": "PT-1005",
        "ram": "8GB",
        "processador": "AMD Ryzen 5 3600",
        "modelo": "Acer Aspire TC",
        "tipo": "Desktop",
        "hd_primario": "256GB SSD",
        "hd_secundario": "1TB HDD"
    },
    {
        "id": 6,
        "user_id": 6,
        "patrimonio": "PT-1006",
        "ram": "16GB",
        "processador": "Intel i7-10700",
        "modelo": "Dell Vostro 3681",
        "tipo": "Desktop",
        "hd_primario": "512GB SSD",
        "hd_secundario": "1TB HDD"
    },
    {
        "id": 7,
        "user_id": 7,
        "patrimonio": "PT-1007",
        "ram": "32GB",
        "processador": "Intel i9-10900K",
        "modelo": "Custom Build",
        "tipo": "Desktop",
        "hd_primario": "1TB SSD",
        "hd_secundario": "2TB HDD"
    },
    {
        "id": 8,
        "user_id": 8,
        "patrimonio": "PT-1008",
        "ram": "8GB",
        "processador": "Intel i3-10100",
        "modelo": "HP EliteDesk 800",
        "tipo": "Desktop",
        "hd_primario": "256GB SSD",
        "hd_secundario": "500GB HDD"
    },
    {
        "id": 9,
        "user_id": 9,
        "patrimonio": "PT-1009",
        "ram": "16GB",
        "processador": "AMD Ryzen 5 5600G",
        "modelo": "Lenovo ThinkCentre M75q",
        "tipo": "Desktop",
        "hd_primario": "512GB SSD",
        "hd_secundario": "1TB HDD"
    },
    {
        "id": 10,
        "user_id": 10,
        "patrimonio": "PT-1010",
        "ram": "32GB",
        "processador": "Intel i7-12700",
        "modelo": "Dell Optiplex 7090",
        "tipo": "Desktop",
        "hd_primario": "1TB SSD",
        "hd_secundario": "2TB HDD"
    }
]

@machines_router.get("/")
def get_machines():
    return machines

@machines_router.get("/{machine_id}")
def get_machine_by_id(machine_id: int):

    for machine in machines:
        if machine["id"] == machine_id:
            return machine

    return machines["machine_id"]