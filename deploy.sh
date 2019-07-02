cd /var/sagefy
./dbbu.sh
cd /var/sagefy
git pull origin master
npm install
npm run dbmate up
docker-compose restart
echo "Was there any changes to .env?"
echo "-- Update your .env; then run the command below"
echo "Any Dockerfile changes? "
echo "--: docker-compose down; docker-compose up --build -d"
