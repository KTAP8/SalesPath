# Use a node image as a base
FROM node:18

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Expose the port the app runs on
EXPOSE 8081

# Run the web server
CMD ["npm", "run", "web"]
