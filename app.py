from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
class DeliveryCalculator:
    def __init__(self):
        self.base_rate = 10
        self.price_per_kg = 3
        self.price_per_km = 2
        self.min_weight = 0.1
        self.max_weight = 1000
        self.min_distance = 1
        self.max_distance = 5000
        self.urgent_multiplier = 1.5
        self.fragile_surcharge = 0.2
        self.insurance_rate = 0.01

    def calculate_cost(self, weight, distance, is_urgent=False, is_fragile=False, insurance_value=0):
        if weight < self.min_weight or weight > self.max_weight:
            raise ValueError(f"Вес должен быть от {self.min_weight} до {self.max_weight} кг")
        if distance < self.min_distance or distance > self.max_distance:
            raise ValueError(f"Расстояние должно быть от {self.min_distance} до {self.max_distance} км")

        cost = self.base_rate + (weight * self.price_per_kg) + (distance * self.price_per_km)
        if is_urgent:
            cost *= self.urgent_multiplier
        if is_fragile:
            cost *= (1 + self.fragile_surcharge)
        if insurance_value > 0:
            cost += insurance_value * self.insurance_rate
        return round(cost, 2)

    def get_detailed_calculation(self, weight, distance, is_urgent=False, is_fragile=False, insurance_value=0):
        details = {}
        base_component = self.base_rate
        weight_component = weight * self.price_per_kg
        distance_component = distance * self.price_per_km
        subtotal = base_component + weight_component + distance_component
        details['base'] = base_component
        details['weight'] = weight_component
        details['distance'] = distance_component
        details['subtotal'] = subtotal
        if is_urgent:
            urgent_cost = subtotal * (self.urgent_multiplier - 1)
            details['urgent'] = urgent_cost
            subtotal *= self.urgent_multiplier
        if is_fragile:
            fragile_cost = subtotal * self.fragile_surcharge
            details['fragile'] = fragile_cost
            subtotal *= (1 + self.fragile_surcharge)
        if insurance_value > 0:
            insurance_cost = insurance_value * self.insurance_rate
            details['insurance'] = insurance_cost
            subtotal += insurance_cost
        details['total'] = round(subtotal, 2)
        return details

calculator = DeliveryCalculator()

@app.route('/delivery/calculate', methods=['POST'])
def calculate_delivery():
    data = request.json
    try:
        weight = float(data.get('weight', 0))
        distance = float(data.get('distance', 0))
        is_urgent = bool(data.get('is_urgent', False))
        is_fragile = bool(data.get('is_fragile', False))
        insurance_value = float(data.get('insurance_value', 0))

        cost = calculator.calculate_cost(weight, distance, is_urgent, is_fragile, insurance_value)
        details = calculator.get_detailed_calculation(weight, distance, is_urgent, is_fragile, insurance_value)
        return jsonify({
            'cost': cost,
            'details': details
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
@app.route('/products', methods=['GET'])
def get_all_products():
    """Получить все товары"""
    try:
        return jsonify({'products': products})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/delivery/rates', methods=['GET'])
def get_rates():
    return jsonify({
        'base_rate': calculator.base_rate,
        'price_per_kg': calculator.price_per_kg,
        'price_per_km': calculator.price_per_km,
        'urgent_multiplier': calculator.urgent_multiplier,
        'fragile_surcharge': calculator.fragile_surcharge,
        'insurance_rate': calculator.insurance_rate,
        'min_weight': calculator.min_weight,
        'max_weight': calculator.max_weight,
        'min_distance': calculator.min_distance,
        'max_distance': calculator.max_distance
    })

if __name__ == '__main__':
    app.run(debug=True, port = 5003)

