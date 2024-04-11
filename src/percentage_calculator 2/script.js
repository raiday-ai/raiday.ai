 <script>
        function findPercentage() {
            var num1 = document.getElementById('num1').value;
            var num2 = document.getElementById('num2').value;
            var result = (num1 / num2) * 100;
            document.getElementById('result2').innerText = result.toFixed(2) + '%';
        }
    </script>