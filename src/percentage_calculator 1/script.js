<script>
        function calculatePercentage() {
            var percentage = document.getElementById('percentage').value;
            var number = document.getElementById('number').value;
            var result = (percentage / 100) * number;
            document.getElementById('result').innerText = result.toFixed(2);
        }
    </script>