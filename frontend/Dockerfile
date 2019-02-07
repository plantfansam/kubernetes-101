FROM alpine:3.9

RUN apk add --update bash yarn
ADD package.json /app/
WORKDIR /app
RUN yarn install

ADD . /app
CMD ["yarn", "start"]