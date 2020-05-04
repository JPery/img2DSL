java -jar Ecore2Use.jar "$1" out.ecore
java -jar Use2Text.jar out.ecore > /dev/null
