<script>
        function calculateChange() {
            var initialValue = parseFloat(document.getElementById('initialValue3').value);
            var finalValue = parseFloat(document.getElementById('finalValue3').value);
            var change = ((finalValue - initialValue) / initialValue) * 100;
            document.getElementById('result3').innerText = change.toFixed(2) + '%';
        }
</script>